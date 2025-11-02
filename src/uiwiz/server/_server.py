import asyncio
from asyncio import Queue, Event, TimerHandle
import re
from typing import Any, Callable, Optional, cast
import urllib
from pydantic import BaseModel
import httptools
import http
import importlib
from dataclasses import dataclass

from uvicorn._types import (
    ASGI3Application,
    ASGIReceiveEvent,
    ASGISendEvent,
    HTTPRequestEvent,
    HTTPResponseStartEvent,
    HTTPScope,
)

from uvicorn.protocols.http.flow_control import CLOSE_HEADER, HIGH_WATER_LIMIT, FlowControl, service_unavailable
from uiwiz.app import UiwizApp
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

HEADER_RE = re.compile(b'[\x00-\x1f\x7f()<>@,;:[]={} \t\\"]')
HEADER_VALUE_RE = re.compile(b"[\x00-\x08\x0a-\x1f\x7f]")

@dataclass
class Config:
    host: str
    port: int
    app: Optional[UiwizApp]
    app_instance: Optional[UiwizApp] = None
    root_path: str


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
        self.root_path = config.root_path
        self.cycle: RequestResponseCycle = None

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

    def eof_received(self) -> None: ...

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

        existing_cycle = self.cycle
        self.cycle = RequestResponseCycle(
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
            task = self.loop.create_task(self.cycle.run_asgi(self.config.app_instance))
            task.add_done_callback(self.tasks.discard)
            self.tasks.add(task)
        else:
            # Pipelined HTTP requests need to be queued up.
            self.flow.pause_reading()
            self.pipeline.appendleft((self.cycle, self.config.app_instance))

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


class RequestResponseCycle:
    def __init__(
        self,
        scope: dict,
        transport: asyncio.Transport,
        default_headers: list,
        message_event: asyncio.Event,
        on_response: Callable,
    ):
        self.scope = scope
        self.transport = transport
        self.default_headers = default_headers
        self.message_event = message_event
        self.on_response = on_response

    async def run_asgi(self, app: ASGI3Application) -> None:
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

    async def send_500_response(self) -> None:
        await self.send(
            {
                "type": "http.response.start",
                "status": 500,
                "headers": [
                    (b"content-type", b"text/plain; charset=utf-8"),
                    (b"content-length", b"21"),
                    (b"connection", b"close"),
                ],
            }
        )
        await self.send({"type": "http.response.body", "body": b"Internal Server Error", "more_body": False})

    # ASGI interface
    async def send(self, message: ASGISendEvent) -> None:
        message_type = message["type"]

        if self.flow.write_paused and not self.disconnected:
            await self.flow.drain()  # pragma: full coverage

        if self.disconnected:
            return  # pragma: full coverage

        if not self.response_started:
            # Sending response status line and headers
            if message_type != "http.response.start":
                msg = "Expected ASGI message 'http.response.start', but got '%s'."
                raise RuntimeError(msg % message_type)
            message = cast("HTTPResponseStartEvent", message)

            self.response_started = True
            self.waiting_for_100_continue = False

            status_code = message["status"]
            headers = self.default_headers + list(message.get("headers", []))

            if CLOSE_HEADER in self.scope["headers"] and CLOSE_HEADER not in headers:
                headers = headers + [CLOSE_HEADER]

            if self.access_log:
                self.access_logger.info(
                    '%s - "%s %s HTTP/%s" %d',
                    get_client_addr(self.scope),
                    self.scope["method"],
                    get_path_with_query_string(self.scope),
                    self.scope["http_version"],
                    status_code,
                )

            # Write response status line and headers
            content = [STATUS_LINE[status_code]]

            for name, value in headers:
                if HEADER_RE.search(name):
                    raise RuntimeError("Invalid HTTP header name.")  # pragma: full coverage
                if HEADER_VALUE_RE.search(value):
                    raise RuntimeError("Invalid HTTP header value.")

                name = name.lower()
                if name == b"content-length" and self.chunked_encoding is None:
                    self.expected_content_length = int(value.decode())
                    self.chunked_encoding = False
                elif name == b"transfer-encoding" and value.lower() == b"chunked":
                    self.expected_content_length = 0
                    self.chunked_encoding = True
                elif name == b"connection" and value.lower() == b"close":
                    self.keep_alive = False
                content.extend([name, b": ", value, b"\r\n"])

            if self.chunked_encoding is None and self.scope["method"] != "HEAD" and status_code not in (204, 304):
                # Neither content-length nor transfer-encoding specified
                self.chunked_encoding = True
                content.append(b"transfer-encoding: chunked\r\n")

            content.append(b"\r\n")
            self.transport.write(b"".join(content))

        elif not self.response_complete:
            # Sending response body
            if message_type != "http.response.body":
                msg = "Expected ASGI message 'http.response.body', but got '%s'."
                raise RuntimeError(msg % message_type)

            body = cast(bytes, message.get("body", b""))
            more_body = message.get("more_body", False)

            # Write response body
            if self.scope["method"] == "HEAD":
                self.expected_content_length = 0
            elif self.chunked_encoding:
                if body:
                    content = [b"%x\r\n" % len(body), body, b"\r\n"]
                else:
                    content = []
                if not more_body:
                    content.append(b"0\r\n\r\n")
                self.transport.write(b"".join(content))
            else:
                num_bytes = len(body)
                if num_bytes > self.expected_content_length:
                    raise RuntimeError("Response content longer than Content-Length")
                else:
                    self.expected_content_length -= num_bytes
                self.transport.write(body)

            # Handle response completion
            if not more_body:
                if self.expected_content_length != 0:
                    raise RuntimeError("Response content shorter than Content-Length")
                self.response_complete = True
                self.message_event.set()
                if not self.keep_alive:
                    self.transport.close()
                self.on_response()

        else:
            # Response already sent
            msg = "Unexpected ASGI message '%s' sent, after response already completed."
            raise RuntimeError(msg % message_type)

    async def receive(self) -> ASGIReceiveEvent:
        if self.waiting_for_100_continue and not self.transport.is_closing():
            self.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")
            self.waiting_for_100_continue = False

        if not self.disconnected and not self.response_complete:
            self.flow.resume_reading()
            await self.message_event.wait()
            self.message_event.clear()

        if self.disconnected or self.response_complete:
            return {"type": "http.disconnect"}
        message: HTTPRequestEvent = {"type": "http.request", "body": self.body, "more_body": self.more_body}
        self.body = b""
        return message


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
    config = Config(host="localhost", port=8080, app="uiwiz.server.main:app", root_path="")

    server = Server(config)
    server.run()
