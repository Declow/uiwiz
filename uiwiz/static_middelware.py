from starlette.middleware.base import BaseHTTPMiddleware


class TtlMiddelware(BaseHTTPMiddleware):
    def __init__(self, app, cache_age: int):
        super().__init__(app)
        self.cahce_age = cache_age

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if "static/" in str(request.url):
            response.headers["Cache-Control"] = f"max-age={self.cahce_age}"
        return response
