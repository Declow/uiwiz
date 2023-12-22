from starlette.datastructures import Headers
from contextvars import ContextVar
from starlette.types import ASGIApp, Receive, Scope, Send

HX_TARGET_CTX_KEY = "headers"

_hx_target_ctx_var: ContextVar[dict] = ContextVar(HX_TARGET_CTX_KEY, default=None)


def get_headers() -> dict[str:str]:
    return _hx_target_ctx_var.get()


class CustomRequestMiddleware:
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http"]:
            await self.app(scope, receive, send)
            return
        headers = Headers(scope=scope)
        _headers = _hx_target_ctx_var.set(headers)

        await self.app(scope, receive, send)

        _hx_target_ctx_var.reset(_headers)
