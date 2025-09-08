from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
import json

class StripHiddenFormFieldMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, field_name: str = "csrf_token"):
        super().__init__(app)
        self.field_name = field_name

    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH") and request.headers.get("content-type", "").startswith("application/json"):
            body: dict = await request.json()
            body.pop(self.field_name, None)
            new_body = json.dumps(body).encode()

            async def receive():
                return {"type": "http.request", "body": new_body, "more_body": False}
            request._receive = receive

        response = await call_next(request)
        return response