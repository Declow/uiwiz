from typing import Any

from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.types import AppType, Receive, Scope, Send


class AsgiTtlMiddleware:
    def __init__(self, app: AppType, cache_age: int) -> None:
        self.app = app
        self.cache_age = cache_age

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:  # noqa: ANN401, RET503
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_with_extra_headers(message) -> None:  # noqa: ANN001
            if message["type"] != "http.response.start":
                await send(message)
                return

            request = Request(scope)
            if request.url.path.startswith("/_static/"):
                headers = MutableHeaders(scope=message)
                headers["Cache-Control"] = f"max-age={self.cache_age}"

            await send(message)

        await self.app(scope, receive, send_with_extra_headers)
