import functools
import inspect
import logging
import os
from html import escape
from mimetypes import guess_type
from pathlib import Path
from typing import Callable, Optional, Union

from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from uiwiz.asgi_request_middelware import AsgiRequestMiddelware
from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.page_route import PageRouter
from uiwiz.static_middelware import AsgiTtlMiddelware

logger = logging.getLogger("uiwiz")
logger.addHandler(logging.NullHandler())


class UiwizApp(FastAPI):
    def __init__(
        self,
        toast_delay: int = 2500,
        error_classes: str = "alert alert-error",
        cache_age: int = 14400,
        theme: Optional[str] = None,
        auth_header: Optional[str] = None,
        title: Optional[str] = "UiWiz",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.toast_delay = toast_delay
        self.error_classes = error_classes
        if theme:
            self.theme = f"data-theme={theme}"
        else:
            self.theme = theme
        self.auth_header = auth_header
        self.title = title
        self.templates = Jinja2Templates(Path(__file__).parent / "templates")
        self.add_static_files("/static", Path(__file__).parent / "static")

        self.add_middleware(AsgiRequestMiddelware)
        self.add_middleware(GZipMiddleware)
        self.add_middleware(AsgiTtlMiddelware, cache_age=cache_age)
        self.extensions: dict[str, Path] = {}
        self.app_paths: dict[str, Path] = {}

        @self.get("/_static/default.js")
        def return_default_js(request: Request):
            return self.render(request, template_name="default.js", media_type="application/javascript")

        @self.exception_handler(RequestValidationError)
        async def handle_validation_error(request: Request, exc: RequestValidationError):
            fields_with_errors = [item.get("loc")[1] for item in exc.errors() if item.get("loc")[1] in exc.body]
            ok_fields = [item for item in exc.body.keys() if item not in fields_with_errors]
            return JSONResponse(
                status_code=422,
                content=jsonable_encoder(
                    {"detail": exc.errors(), "fieldErrors": fields_with_errors, "fieldOk": ok_fields}
                ),
            )

    def __get_title__(self, frame: Frame, route_title: Optional[str] = None) -> str:
        title = self.title

        if route_title:
            title = route_title

        if dynamic_title := frame.title:
            title = dynamic_title

        return title

    def render(
        self,
        request: Request,
        title: Optional[str] = None,
        status_code: int = 200,
        template_name: str = "default.html",
        media_type: Optional[str] = None,
    ):
        frame = Frame.get_stack()
        html = frame.render()
        ext = frame.render_ext()
        page_title = self.__get_title__(frame, title)
        theme = self.theme
        if cookie_theme := request.cookies.get("data-theme"):
            theme = f"data-theme={escape(cookie_theme)}"
        return self.return_funtion_response(
            self.templates.TemplateResponse(
                name=template_name,
                context={
                    "request": request,
                    "root_element": [html],
                    "title": page_title,
                    "theme": theme,
                    "ext": ext,
                    "toast_delay": self.toast_delay,
                    "error_classes": self.error_classes,
                    "auth_header_name": self.auth_header,
                    "description_content": frame.meta_description_content,
                },
                status_code=status_code,
                headers={"Cache-Control": "no-store", "X-uiwiz-Content": "page"},
                media_type=media_type,
            )
        )

    def render_api(self, status_code: int = 200):
        return self.return_funtion_response(
            HTMLResponse(
                Frame.get_stack().render(),
                status_code,
                {"Cache-Control": "no-store", "X-uiwiz-Content": "partial-ui"},
            )
        )

    def route_exists(self, path: str) -> None:
        return path in list(self.app_paths.values())

    def remove_route(self, path: str) -> None:
        """Remove routes with the given path."""
        self.routes[:] = [r for r in self.routes if getattr(r, "path", None) != path]

    def add_static_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        self.mount(url_path, StaticFiles(directory=str(local_directory)))

    def register_extension(self, path: Path, prefix: str):
        _, filename = os.path.split(path)
        if filename in self.extensions:
            return
        self.extensions[filename] = path

        def get_extension(filename):
            if filename not in self.extensions:
                return Response(status_code=404)

            with open(self.extensions[filename]) as f:
                content = f.read()

            content_type, _ = guess_type(filename)
            return Response(content, media_type=content_type)

        self.get(prefix + "{filename}")(get_extension)

    def post(self, path: str, *args, **kwargs):
        s = super()

        @functools.wraps(s.post)
        def decorator(func: Callable, *args, **kwargs) -> Callable:
            if not self.route_exists(path):
                self.app_paths[func] = path
            return s.post(path, *args, **kwargs)(func)

        return decorator

    def page(
        self,
        path: str,
        *args,
        title: Optional[str] = None,
        favicon: Optional[str] = None,
    ) -> Callable:
        def decorator(func: Callable, *args, **kwargs) -> Callable:
            self.remove_route(path)
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                # Create frame before function is called
                Frame.get_stack()
                Element().classes("flex flex-col min-h-screen h-full")
                request = dec_kwargs["request"]
                # NOTE cleaning up the keyword args so the signature is consistent with "func" again
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):
                    return self.return_funtion_response(result)

                return self.render(request, title)

            params = [p for p in inspect.signature(func).parameters.values()]
            if "request" not in {p.name for p in params}:
                request = inspect.Parameter(
                    "request",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Request,
                )
                params.insert(0, request)
            decorated.__signature__ = inspect.Signature(params)

            if not self.route_exists(path):
                self.app_paths[decorated] = path

            return self.get(path)(decorated)

        return decorator

    def ui(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.remove_route(path)
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                # Create frame before function is called
                Frame.get_stack()
                # NOTE cleaning up the keyword args so the signature is consistent with "func" again
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                    return self.return_funtion_response(result)

                return self.render_api()

            request = inspect.Parameter("request", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Request)
            params = [p for p in inspect.signature(func).parameters.values()]
            for p in params:
                if p.annotation == inspect.Signature.empty:
                    p._annotation = Request
            if "request" not in {p.name for p in params}:
                params.insert(0, request)
            decorated.__signature__ = inspect.Signature(params)

            if not self.route_exists(path):
                self.app_paths[decorated] = path

            return self.post(path)(decorated)

        return decorator

    def add_page_router(self, page_router: PageRouter):
        for key, value in page_router.paths.items():
            if not self.route_exists(key):
                self.app_paths[value.get("func")] = key
            type = value.get("type")
            if type == "page":
                self.page(key, *value.get("args"), **value.get("kwargs"))(value.get("func"))
            if type == "ui":
                self.ui(key)(value.get("func"))

    def return_funtion_response(self, response: Response) -> Response:
        Frame.get_stack().del_stack()
        return response
