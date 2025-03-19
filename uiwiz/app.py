import json
import logging
from html import escape
from mimetypes import guess_type
from pathlib import Path
from typing import Optional, Union

from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from starlette.requests import Request

from uiwiz.asgi_request_middleware import AsgiRequestMiddleware
from uiwiz.element import Element
from uiwiz.elements.button import Button
from uiwiz.elements.col import Col
from uiwiz.elements.html import Html
from uiwiz.frame import Frame
from uiwiz.page_route import PageRouter
from uiwiz.shared import register_path, resources
from uiwiz.static_middleware import AsgiTtlMiddleware
from uiwiz.version import __version__

logger = logging.getLogger("uiwiz")
logger.addHandler(logging.NullHandler())


class CustomList(list):
    def append(self, route: APIRoute):
        if getattr(route, "endpoint", None):
            register_path(route.path, route.endpoint)
        return super().append(route)


class UiwizApp(FastAPI):
    def __init__(
        self,
        toast_delay: int = 2500,
        error_classes: str = "alert alert-error",
        cache_age: int = 14400,
        theme: Optional[str] = None,
        title: Optional[str] = "UiWiz",
        auto_close_toast_error: bool = False,
        *args,
        **kwargs,
    ) -> None:
        """App used for asgi applications

        See fastapi documentation for more *args and **kwargs
        
        :param toast_delay: The time in milliseconds before the toast is removed
        :param error_classes: The classes to apply to the toast error for default validation errors
        :param cache_age: The time in seconds to cache the static files
        :param theme: The default theme to use
        :param title: The default title for the app
        :param auto_close_toast_error: If the toast error should auto close
        :param args: FastAPI args
        :param kwargs: FastAPI kwargs
        """
        super().__init__(*args, **kwargs)
        self.router.routes = CustomList()
        self.toast_delay = toast_delay
        self.error_classes = error_classes
        self.auto_close_toast_error = auto_close_toast_error
        if theme:
            self.theme = f"data-theme={theme}"
        else:
            self.theme = theme
        self.title = title
        self.templates = Jinja2Templates(Path(__file__).parent / "templates")
        self.add_static_files(f"/_static/{__version__}/", Path(__file__).parent / "static")

        self.add_middleware(AsgiRequestMiddleware)
        self.add_middleware(GZipMiddleware)
        self.add_middleware(AsgiTtlMiddleware, cache_age=cache_age)
        self.extensions: dict[str, Path] = {}
        self.app_paths: dict[str, Path] = {}

        @self.get(f"/_uiwiz/{__version__}/default.js", include_in_schema=False)
        def return_default_js(request: Request, response: Response):
            response.headers["cache-control"] = f"max-age={cache_age}"
            response.headers["x-uiwiz-content"] = "assets"
            return self.render(request, response, template_name="default.js", media_type="application/javascript")

        self.exception_handler(RequestValidationError)(self.handle_validation_error)
        

        @self.get("/_static/extension/{__version__}/{extension}/{filename}", include_in_schema=False)
        def get_extension(extension: str, filename: str):
            resource_key = f"{extension}/{filename}"
            if resource_key not in resources:
                return Response(status_code=404)

            with open(resources[resource_key], encoding="utf-8") as f:
                content = f.read()

            content_type, _ = guess_type(resource_key)
            return Response(content, media_type=content_type)

    def __get_title__(self, frame: Frame, route_title: Optional[str] = None) -> str:
        title = self.title

        if route_title:
            title = route_title

        if dynamic_title := frame.title:
            title = dynamic_title

        return title

    def add_static_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        self.mount(url_path, StaticFiles(directory=str(local_directory)))

    def page(
        self, path: str, *args, title: Optional[str] = None, favicon: Optional[str] = None, **kwargs
    ) -> PageRouter:
        return PageRouter().page(path, *args, title=title, favicon=favicon, router=self.router, **kwargs)

    def ui(self, path: str, *args, include_js: bool = True, include_css: bool = True, **kwargs) -> PageRouter:
        return PageRouter().ui(path=path, include_js=include_js, include_css=include_css, router=self.router, **kwargs)

    def render(
        self,
        request: Request,
        response: Response,
        title: Optional[str] = None,
        status_code: int = 200,
        template_name: str = "default.html",
        media_type: str = "text/html",
        root_overflow: str = "overflow-y: scroll",
    ):
        frame = Frame.get_stack()
        ext_js, ext_css = frame.render_ext()

        theme = self.theme
        if cookie_theme := request.cookies.get("data-theme"):
            theme = f"data-theme={escape(cookie_theme)}"

        root_overflow = f'style="{root_overflow}"'
        standard_headers = {"cache-control": "no-store", "x-uiwiz-content": "page"}
        default_page: Template = self.templates.get_template(template_name)

        if response:
            for key, value in response.headers.items():
                standard_headers[key] = value

        return self.return_funtion_response(
            HTMLResponse(
                content=default_page.render(
                    request=request,
                    root_element=[frame.render()],
                    title=self.__get_title__(frame, title),
                    theme=theme,
                    ext_js=ext_js,
                    ext_css=ext_css,
                    toast_delay=json.dumps({"delay": self.toast_delay}),
                    description_content=frame.meta_description_content,
                    overflow=root_overflow,
                    head=frame.head_ext,
                    version=__version__,
                ),
                status_code=status_code,
                headers=standard_headers,
                media_type=media_type,
            )
        )

    def return_funtion_response(self, response: Union[str, Response]) -> Union[str, Response]:
        Frame.get_stack().del_stack()
        return response

    async def handle_validation_error(self, request: Request, exc: RequestValidationError):
        fields_with_errors = [item.get("loc")[1] for item in exc.errors() if item.get("loc")[1] in exc.body]
        ok_fields = [item for item in exc.body.keys() if item not in fields_with_errors]

        Frame.get_stack().del_stack()
        Frame.get_stack()
        
        with Element().classes(self.error_classes) as toast:
            toast.attributes["id"] = "toast"
            toast.attributes["hx-swap-oob"] = "afterbegin"
            toast.attributes["hx-toast-data"] = json.dumps(jsonable_encoder(
                {
                    "detail": exc.errors(),
                    "fieldErrors": fields_with_errors,
                    "fieldOk": ok_fields,
                }
            ))
            html = Html("").classes("alert alert-error relative")
            html.tag = "span"
            html.attributes["hx-toast-data"] = json.dumps({"autoClose": self.auto_close_toast_error})
            html.attributes["hx-toast-delete-button"] = lambda: btn.id
            with html:
                with Col(gap="").classes("relative"):
                    for item in exc.errors():
                        Element(content=f"{item.get('loc')[1]}: {item.get('msg')}")
                if not self.auto_close_toast_error:
                    btn = Button("✕").classes("btn btn-sm btn-circle btn-ghost absolute right-2 top-2")
                    
        html_content = Frame.get_stack().render()


        return HTMLResponse(
            content=html_content,
            status_code=200,
            headers={"cache-control": "no-store", "x-uiwiz-content": "page", "x-uiwiz-validation-error": "true"},
        )