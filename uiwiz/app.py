import inspect
from mimetypes import guess_type
import os
from pathlib import Path
from typing import Callable, Optional, Union
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from uiwiz.element import Element, Frame
from fastapi.middleware.gzip import GZipMiddleware
from uiwiz.header_middelware import CustomRequestMiddleware
import functools
import logging
from uiwiz.page_route import PageRouter

logger = logging.getLogger("uiwiz")
logger.addHandler(logging.NullHandler())


class UiwizApp(FastAPI):
    app_paths = {}

    def __init__(
        self,
        toast_delay: int = 2500,
        error_classes: str = "alert bg-[#FF8080]",
        theme: Optional[str] = None,
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
        self.templates = Jinja2Templates(Path(__file__).parent / "templates")
        self.add_static_files("/static", Path(__file__).parent / "static")
        Frame.api = self
        self.add_middleware(CustomRequestMiddleware)
        self.add_middleware(GZipMiddleware)
        self.extensions: dict[str, Path] = {}

    def render(
        self,
        frame: Frame,
        request: Request,
        title: str,
        status_code: int = 200,
    ):
        html = frame.render()
        libs = frame.render_libs()
        ext = frame.render_ext()
        frame.del_stack()
        return self.templates.TemplateResponse(
            "default.html",
            {
                "request": request,
                "root_element": [html],
                "title": title,
                "theme": self.theme,
                "libs": libs,
                "ext": ext,
                "toast_delay": self.toast_delay,
                "error_classes": self.error_classes,
            },
            status_code,
            {"Cache-Control": "no-store", "X-uiwiz-Content": "page"},
        )

    def render_api(self, frame: Frame, status_code: int = 200):
        html = frame.render()
        frame.del_stack()
        return HTMLResponse(
            html,
            status_code,
            {"Cache-Control": "no-store", "X-uiwiz-Content": "page"},
        )

    def route_exists(self, path: str) -> None:
        return path in self.routes

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

        def decorator(func: Callable, *args, **kwargs) -> Callable:
            self.app_paths[func] = path
            return s.post(path, *args, **kwargs)(func)

        return decorator

    def page(
        self,
        path: str,
        *args,
        title: Optional[str] = "uiwiz",
        favicon: Optional[str] = None,
    ) -> Callable:
        def decorator(func: Callable, *args, **kwargs) -> Callable:
            self.remove_route(path)
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            async def decorated(*dec_args, **dec_kwargs) -> Response:
                frame: Frame = Frame.get_stack()
                frame.app = self
                Element().classes("flex flex-col h-screen")
                request = dec_kwargs["request"]
                # NOTE cleaning up the keyword args so the signature is consistent with "func" again
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                    return result

                return self.render(frame, request, title)

            params = [p for p in inspect.signature(func).parameters.values()]
            if "request" not in {p.name for p in params}:
                request = inspect.Parameter(
                    "request",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Request,
                )
                params.insert(0, request)
            decorated.__signature__ = inspect.Signature(params)

            self.app_paths[decorated] = path

            return self.get(path)(decorated)

        return decorator

    def ui(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.remove_route(path)
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                frame = Frame.get_stack()
                # NOTE cleaning up the keyword args so the signature is consistent with "func" again
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                    return result

                return self.render_api(frame)

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

    def include_page_router(self, page_router: PageRouter):
        for key, value in page_router.paths.items():
            type = value.get("type")
            if type == "page":
                self.page(key)(value.get("func"))
            if type == "ui":
                self.ui(key)(value.get("func"))
