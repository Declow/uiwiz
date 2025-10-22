import asyncio
from asyncio import Queue, Event, TimerHandle
from typing import Any, Optional
from pydantic import BaseModel
import httptools
import http
import importlib
from dataclasses import dataclass

from uiwiz.app import UiwizApp
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@dataclass
class Config:
    host: str
    port: int
    app: Optional[UiwizApp]
    app_instance: Optional[UiwizApp] = None

def import_app_instance(config: Config) -> None:
    if isinstance(config.app, str):
        module_name, _, app = config.app.partition(":")
        module = importlib.import_module(module_name)
        config.app_instance = getattr(module, app)
    else:
        config.app_instance = config.app

class LifespanHandler:
    def __init__(self, config: Config):
        self.config = config
        self.receive_queue: Queue = Queue()
        self.state: dict[str, Any] = {}
        self.startup_done_event = Event()
        self.shutdown_done_event = Event()

    async def startup(self) -> None:
        logger.info("Calling lifespan")
        loop = asyncio.get_running_loop()
        lifespan_task = loop.create_task(self.execute())
        await self.receive_queue.put({"type": "lifespan.startup"})
        await self.startup_done_event.wait()

        logger.info("Startup complete")

    async def execute(self) -> None:
        app = self.config.app_instance
        scope = {
            "type": "lifespan",
            "asgi": {"version": "3", "spec_version": "2.0"},
            "state": self.state,
        }
        await app(scope, self.receive_queue, self.send)

    async def send(self, message: dict) -> None:
        task = {
            "lifespan.startup.complete": lambda: self.startup_done_event.set(),
            "lifespan.startup.failed": lambda: self.startup_done_event.set(),
            "lifespan.shutdown.complete": lambda: self.shutdown_done_event.set(),
            "lifespan.shutdown.failed": lambda: self.shutdown_done_event.set(),
        }
        task.get(message["type"], lambda: 1)()


class HttpToolsImpl(asyncio.Protocol):
    def __init__(self, config: Config):
        self.config = config
        self.lifespan = LifespanHandler(config)
        self.app = config.app
        self.state: dict[str, Any] = {}
        self.loop = asyncio.get_event_loop()
        self.parser = httptools.HttpRequestParser(self)
        self.timeout_keep_alive_task: TimerHandle | None = None
        self.transport: asyncio.Transport = None
        self.app_state = dict()
        # self.cycle: RequestResponseCycle = None

    def data_received(self, data: bytes) -> None:
        self._unset_keepalive_if_required()
        logger.info("Got request")

        try:
            self.parser.feed_data(data)
        except httptools.HttpParserError:
            msg = "Invalid HTTP request received."
            logger.warning(msg)
            self.send_400_response(msg)
            return
        except httptools.HttpParserUpgrade:
            if self._should_upgrade():
                self.handle_websocket_upgrade()
            else:
                self._unsupported_upgrade_warning()

    def eof_received(self) -> None:
        ...

    def _unset_keepalive_if_required(self) -> None:
        if self.timeout_keep_alive_task is not None:
            self.timeout_keep_alive_task.cancel()
            self.timeout_keep_alive_task = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport
        # self.flow = FlowControl(transport) should not be relevant
        self.server = self.get_local_addr()
        self.client = self.get_remote_addr()
        self.scheme = "https" if bool(transport.get_extra_info("sslcontext")) else "http"

    def connection_lost(self, exc: Exception | None) -> None:

        if self.cycle and not self.cycle.response_complete:
            self.cycle.disconnected = True
        if self.cycle is not None:
            self.cycle.message_event.set()
        if self.flow is not None:
            self.flow.resume_writing()
        if exc is None:
            self.transport.close()
            self._unset_keepalive_if_required()

        self.parser = None

    def on_url(self, url: bytes) -> None:
        self.url += url
    
    def on_header(self, name: bytes, value: bytes) -> None:
        name = name.lower()
        if name == b"expect" and value.lower() == b"100-continue":
            self.expect_100_continue = True
        self.headers.append((name, value))



    def on_message_begin(self) -> None:
        import_app_instance(config)
        # asyncio.get_running_loop().create_task(self.lifespan.startup())

        self.url = b""
        self.expect_100_continue = False
        self.headers = []
        self.scope = {  # type: ignore[typeddict-item]
            "type": "http",
            "asgi": {"version": "asgi3", "spec_version": "2.3"},
            "http_version": "1.1",
            "server": self.server,
            "client": self.client,
            "scheme": self.scheme,  # type: ignore[typeddict-item]
            "root_path": "",
            "headers": self.headers,
            "state": self.app_state,
        }


    def on_response_complete(self) -> None:
        if self.transport.is_closing():
            return

        self._unset_keepalive_if_required()

        # Unpause data reads if needed.
        self.flow.resume_reading()

        # Unblock any pipelined events. If there are none, arm the
        # Keep-Alive timeout instead.
        if self.pipeline:
            cycle, app = self.pipeline.pop()
            task = self.loop.create_task(cycle.run_asgi(app))
            task.add_done_callback(self.tasks.discard)
            self.tasks.add(task)
        else:
            self.timeout_keep_alive_task = self.loop.call_later(
                self.timeout_keep_alive, self.timeout_keep_alive_handler
            )

    def _get_upgrade(self) -> Optional[bytes]:
        connection = []
        upgrade = None
        for name, value in self.headers:
            if name == b"connection":
                connection = [token.lower().strip() for token in value.split(b",")]
            if name == b"upgrade":
                upgrade = value.lower()
        if b"upgrade" in connection:
            return upgrade
        return None  # pragma: full coverage

    def _should_upgrade_to_ws(self) -> bool:
        if self.ws_protocol_class is None:
            return False
        return True

    def _unsupported_upgrade_warning(self) -> None:
        logger.warning("Unsupported upgrade request.")
        if not self._should_upgrade_to_ws():
            msg = "No supported WebSocket library detected. Please use \"pip install 'uvicorn[standard]'\", or install 'websockets' or 'wsproto' manually."  # noqa: E501
            logger.warning(msg)

    def _should_upgrade(self) -> bool:
        upgrade = self._get_upgrade()
        return upgrade == b"websocket" and self._should_upgrade_to_ws()


    def get_local_addr(self) -> Optional[tuple[str, int]]:
        socket_info = self.transport.get_extra_info("socket")
        if socket_info is not None:
            info = socket_info.getsockname()

            return (str(info[0]), int(info[1])) if isinstance(info, tuple) else None
        info = self.transport.get_extra_info("sockname")
        if info is not None and isinstance(info, (list, tuple)) and len(info) == 2:
            return (str(info[0]), int(info[1]))
        return None
    

    def get_remote_addr(self) -> Optional[tuple[str, int]]:
        socket_info = self.transport.get_extra_info("socket")
        if socket_info is not None:
            try:
                info = socket_info.getpeername()
                return (str(info[0]), int(info[1])) if isinstance(info, tuple) else None
            except OSError:
                return None

        info = self.transport.get_extra_info("peername")
        if info is not None and isinstance(info, (list, tuple)) and len(info) == 2:
            return (str(info[0]), int(info[1]))
        return None
    
    def send_400_response(self, msg: str) -> None:
        message = [http.HTTPStatus(400).phrase.encode()]
        # for name, value in self.server_state.default_headers:
        #     message.extend([name, b": ", value, b"\r\n"])  # pragma: full coverage
        message.extend(
            [
                b"content-type: text/plain; charset=utf-8\r\n",
                b"content-length: " + str(len(msg)).encode("ascii") + b"\r\n",
                b"connection: close\r\n",
                b"\r\n",
                msg.encode("ascii"),
            ]
        )
        self.transport.write(b"".join(message))
        self.transport.close()


class Server:
    def __init__(self, config: Config):
        self.config = config
        import_app_instance(config)

    def run(self) -> None:
        return asyncio.run(self._serve(), debug=True)
    
    async def _serve(self) -> None:
        server = await asyncio.get_running_loop().create_server(
            lambda: HttpToolsImpl(self.config),
            host=self.config.host,
            port=self.config.port
        )
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    config = Config(
        host="localhost",
        port=8080,
        app="uiwiz.server.main:app"
    )

    server = Server(config)
    server.run()