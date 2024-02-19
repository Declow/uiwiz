from contextvars import ContextVar
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_CTX_KEY = "_request"

_request_ctx_var: ContextVar[dict[str, Request]] = ContextVar(REQUEST_CTX_KEY, default=None)


def get_request() -> Request:
    return _request_ctx_var.get()


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        _request = _request_ctx_var.set(request)
        response = await call_next(request)
        _request_ctx_var.reset(_request)

        return response
