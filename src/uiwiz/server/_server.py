import asyncio
from asyncio import Queue, Event, TimerHandle
import re
from typing import Any, Optional
import urllib
import httptools
import http
import importlib
from dataclasses import dataclass
from collections import deque

from uvicorn._types import (
    ASGI3Application,
)
from uvicorn.protocols.http.flow_control import FlowControl
from uvicorn.protocols.http.httptools_impl import RequestResponseCycle
from time import perf_counter

from uvicorn.protocols.http.flow_control import HIGH_WATER_LIMIT
from uiwiz.app import UiwizApp
import logging

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
sc = logging.StreamHandler()
sc.setFormatter(formatter)
logger.addHandler(sc)

HEADER_RE = re.compile(b'[\x00-\x1f\x7f()<>@,;:[]={} \t\\"]')
HEADER_VALUE_RE = re.compile(b"[\x00-\x08\x0a-\x1f\x7f]")

@dataclass
class Config:
    host: str
    port: int
    root_path: str
    app: Optional[UiwizApp]
    app_instance: Optional[UiwizApp] = None


def import_app_instance(config: Config) -> None:
    start = perf_counter()
    if isinstance(config.app, str):
        module_name, _, app = config.app.partition(":")
        
        module = importlib.import_module(module_name)
        module = importlib.reload(module)
        config.app_instance = getattr(module, app)
    else:
        config.app_instance = config.app
    end = perf_counter()
    logger.info(f"Module reloaded in: {end - start}")


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

    async def shutdown(self) -> None:
        logger.info("Waiting for application shutdown.")
        shutdown_event = {"type": "lifespan.shutdown"}
        await self.receive_queue.put(shutdown_event)
        await self.shutdown_done_event.wait()

        # if self.shutdown_failed or (self.error_occured and self.config.lifespan == "on"):
        #     self.logger.error("Application shutdown failed. Exiting.")
        #     self.should_exit = True
        # else:
        logger.info("Application shutdown complete.")

    async def execute(self) -> None:
        app = self.config.app_instance
        scope = {
            "type": "lifespan",
            "asgi": {"version": "3", "spec_version": "2.0"},
            "state": self.state,
        }
        await app(scope, self.receive, self.send)

    async def send(self, message: dict) -> None:
        task = {
            "lifespan.startup.complete": lambda: self.startup_done_event.set(),
            "lifespan.startup.failed": lambda: self.startup_done_event.set(),
            "lifespan.shutdown.complete": lambda: self.shutdown_done_event.set(),
            "lifespan.shutdown.failed": lambda: self.shutdown_done_event.set(),
        }
        task.get(message["type"], lambda: 1)()

    async def receive(self):
        return await self.receive_queue.get()

class ServerState:
    def __init__(self):
        self.total_requests = 0
        self.connections = set()
        self.tasks: set[asyncio.Task[None]] = set()
        self.default_headers: list[tuple[bytes, bytes]] = []

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
        self.root_path = config.root_path
        self.cycle: RequestResponseCycle = None

        self.timeout_keep_alive = 10

        self.flow: FlowControl = None  # type: ignore[assignment]
        self.pipeline: deque[tuple[RequestResponseCycle, ASGI3Application]] = deque()
        self.logger = logger
        self.access_logger = logger
        self.access_log = logger.hasHandlers()
        self.server_state = ServerState()
        self.tasks = self.server_state.tasks

    def data_received(self, data: bytes) -> None:
        self._unset_keepalive_if_required()

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

    def eof_received(self) -> None: ...

    def _unset_keepalive_if_required(self) -> None:
        if self.timeout_keep_alive_task is not None:
            self.timeout_keep_alive_task.cancel()
            self.timeout_keep_alive_task = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport
        self.flow = FlowControl(transport)
        self.server = self.get_local_addr()
        self.client = self.get_remote_addr()
        self.scheme = "https" if bool(transport.get_extra_info("sslcontext")) else "http"

    def connection_lost(self, exc: Optional[Exception]) -> None:
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

    def on_headers_complete(self) -> None:
        http_version = self.parser.get_http_version()
        method = self.parser.get_method()
        self.scope["method"] = method.decode("ascii")
        if http_version != "1.1":
            self.scope["http_version"] = http_version
        if self.parser.should_upgrade() and self._should_upgrade():
            return
        parsed_url = httptools.parse_url(self.url)
        raw_path = parsed_url.path
        path = raw_path.decode("ascii")
        if "%" in path:
            path = urllib.parse.unquote(path)
        full_path = self.root_path + path
        full_raw_path = self.root_path.encode("ascii") + raw_path
        self.scope["path"] = full_path
        self.scope["raw_path"] = full_raw_path
        self.scope["query_string"] = parsed_url.query or b""

        import_app_instance(config)
        startup_task = self.loop.create_task(self.lifespan.startup())

        existing_cycle = self.cycle
        self.cycle = RRCycle(
            scope=self.scope,
            transport=self.transport,
            flow=self.flow,
            logger=self.logger,
            access_logger=self.access_logger,
            access_log=self.access_log,
            default_headers=self.server_state.default_headers,
            message_event=asyncio.Event(),
            expect_100_continue=self.expect_100_continue,
            keep_alive=http_version != "1.0",
            on_response=self.on_response_complete,
        )
        if existing_cycle is None or existing_cycle.response_complete:
            # Standard case - start processing the request.
            startup_task.add_done_callback(self.run_asgi_when_done)
            self.tasks.add(startup_task)
            pass
        else:
            # Pipelined HTTP requests need to be queued up.
            self.flow.pause_reading()
            self.pipeline.appendleft((self.cycle, self.config.app_instance))

    def run_asgi_when_done(self, task):
        task = self.loop.create_task(self.cycle.run_asgi(self.config.app_instance))
        task.add_done_callback(self._shutdown)
        self.tasks.add(task)

    def _shutdown(self, *args):
        task = self.loop.create_task(self.lifespan.shutdown())
        task.add_done_callback(self.tasks.discard)
        self.tasks.add(task)

        done = {ta for ta in set(self.tasks) if ta.done()}
        self.tasks.difference_update(done)

    def on_message_begin(self) -> None:
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


    def shutdown(self) -> None:
        """
        Called by the server to commence a graceful shutdown.
        """
        if self.cycle is None or self.cycle.response_complete:
            self.transport.close()
        else:
            self.cycle.keep_alive = False

    def on_body(self, body: bytes) -> None:
        if (self.parser.should_upgrade() and self._should_upgrade()) or self.cycle.response_complete:
            return
        self.cycle.body += body
        if len(self.cycle.body) > HIGH_WATER_LIMIT:
            self.flow.pause_reading()
        self.cycle.message_event.set()


    def on_message_complete(self) -> None:
        if (self.parser.should_upgrade() and self._should_upgrade()) or self.cycle.response_complete:
            return
        self.cycle.more_body = False
        self.cycle.message_event.set()

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

    def pause_writing(self) -> None:
        """
        Called by the transport when the write buffer exceeds the high water mark.
        """
        self.flow.pause_writing()  # pragma: full coverage

    def resume_writing(self) -> None:
        """
        Called by the transport when the write buffer drops below the low water mark.
        """
        self.flow.resume_writing()  # pragma: full coverage

    def timeout_keep_alive_handler(self) -> None:
        """
        Called on a keep-alive connection if no new data is received after a short
        delay.
        """
        if not self.transport.is_closing():
            self.transport.close()

class RRCycle(RequestResponseCycle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ASGI exception wrapper
    async def run_asgi(self, app: ASGI3Application) -> None:
        print("Run asgi")
        try:
            result = await app(  # type: ignore[func-returns-value]
                self.scope, self.receive, self.send
            )
        except BaseException as exc:
            msg = "Exception in ASGI application\n"
            self.logger.error(msg, exc_info=exc)
            if not self.response_started:
                await self.send_500_response()
            else:
                self.transport.close()
        else:
            if result is not None:
                msg = "ASGI callable should return None, but returned '%s'."
                self.logger.error(msg, result)
                self.transport.close()
            elif not self.response_started and not self.disconnected:
                msg = "ASGI callable returned without starting response."
                self.logger.error(msg)
                await self.send_500_response()
            elif not self.response_complete and not self.disconnected:
                msg = "ASGI callable returned without completing response."
                self.logger.error(msg)
                self.transport.close()
        finally:
            self.on_response = lambda: None


class Server:
    def __init__(self, config: Config):
        self.config = config
        import_app_instance(config)

    def run(self) -> None:
        return asyncio.run(self._serve(), debug=True)

    async def _serve(self) -> None:
        server = await asyncio.get_running_loop().create_server(
            lambda: HttpToolsImpl(self.config), host=self.config.host, port=self.config.port
        )
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    import threading
    import time

    def run():
        while True:
            print(1)
            time.sleep(2)
    start = time.perf_counter()
    t = threading.Thread(target=run)
    t.start()
    end = time.perf_counter()
    print(f"thread start time: {(end - start):2f}")



    config = Config(host="localhost", port=8080, app="uiwiz.server.main:app", root_path="")

    server = Server(config)
    server.run()
