from contextvars import ContextVar
from starlette.requests import Request
from typing import Any
from starlette.types import ASGIApp, Receive, Scope, Send

REQUEST_CTX_KEY = "_request"

_request_ctx_var: ContextVar[dict[str, Request]] = ContextVar(REQUEST_CTX_KEY, default=None)


def get_request() -> Request:
    return _request_ctx_var.get()


class AsgiRequestMiddelware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        if scope["type"] == "http":
            request = Request(scope)
            _request_ctx_var.set(request)

        await self.app(scope, receive, send)
