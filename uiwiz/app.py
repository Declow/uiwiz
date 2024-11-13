import functools
import inspect
import logging
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
from jinja2 import Template
from starlette.requests import Request

from uiwiz.asgi_request_middelware import AsgiRequestMiddelware
from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.page_route import PageRouter, PathDefinition
from uiwiz.shared import resources
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

        @self.get("/_static/default.js", include_in_schema=False)
        def return_default_js(request: Request, response: Response):
            response.headers["cache-control"] = f"max-age={cache_age}"
            response.headers["x-uiwiz-content"] = "assets"
            return self.render(request, response, template_name="default.js", media_type="application/javascript")

        @self.exception_handler(RequestValidationError)
        async def handle_validation_error(request: Request, exc: RequestValidationError):
            fields_with_errors = [item.get("loc")[1] for item in exc.errors() if item.get("loc")[1] in exc.body]
            ok_fields = [item for item in exc.body.keys() if item not in fields_with_errors]
            message = " <br> ".join(
                [f"{item.get('loc')[1]}: {item.get('msg')}" for item in exc.errors() if item.get("loc")[1] in exc.body]
            )
            return JSONResponse(
                status_code=422,
                content=jsonable_encoder(
                    {
                        "detail": exc.errors(),
                        "fieldErrors": fields_with_errors,
                        "fieldOk": ok_fields,
                        "message": message,
                    }
                ),
            )

        @self.get("/_static/extension/{extension}/{filename}", include_in_schema=False)
        def get_extension(extension: str, filename: str):
            resource_key = f"{extension}/{filename}"
            if resource_key not in resources:
                return Response(status_code=404)

            with open(resources[resource_key]) as f:
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
                    toast_delay=self.toast_delay,
                    error_classes=self.error_classes,
                    auth_header_name=self.auth_header,
                    description_content=frame.meta_description_content,
                    overflow=root_overflow,
                    head=frame.head_ext,
                ),
                status_code=status_code,
                headers=standard_headers,
                media_type=media_type,
            )
        )

    def route_exists(self, path: str) -> None:
        return path in list(self.app_paths.values())

    def add_static_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        self.mount(url_path, StaticFiles(directory=str(local_directory)))

    def post(self, path: str, *args, **kwargs):
        s = super()

        @functools.wraps(s.post)
        def decorator(func: Callable, *ags, **kvargs) -> Callable:
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
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                Frame.get_stack().del_stack()
                # Create frame before function is called
                Frame.get_stack()
                Element().classes("flex flex-col min-h-screen h-full")
                request = dec_kwargs["request"]
                response = dec_kwargs["response"]

                # NOTE Ensure the signature matches the parameters of the function
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result

                if isinstance(result, Response):
                    return self.return_funtion_response(result)

                return self.render(request, response, title)

            self.__ensure_request_response_signature__(decorated)

            if not self.route_exists(path):
                self.app_paths[decorated] = path

            return self.get(path, include_in_schema=False)(decorated)

        return decorator

    def ui(self, path: str, include_js: bool = True, include_css: bool = True) -> Callable:
        def decorator(func: Callable) -> Callable:
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                Frame.get_stack().del_stack()
                # Create frame before function is called
                Frame.get_stack()
                response = dec_kwargs["response"]

                # NOTE Ensure the signature matches the parameters of the function
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result

                if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                    return self.return_funtion_response(result)

                standard_headers = {"cache-control": "no-store", "x-uiwiz-content": "partial-ui"}
                for key, value in response.headers.items():
                    standard_headers[key] = value

                render = [Frame.get_stack().render()]
                js, css = Frame.get_stack().render_ext()
                if include_css:
                    render.append(css)
                if include_js:
                    render.append(js)
                content = "".join(render)

                return self.return_funtion_response(HTMLResponse(content=content, headers=standard_headers))

            self.__ensure_request_response_signature__(decorated)

            if not self.route_exists(path):
                self.app_paths[decorated] = path

            return self.post(path, include_in_schema=False)(decorated)

        return decorator

    def add_page_router(self, page_router: PageRouter):
        value: PathDefinition
        for key, value in page_router.paths.items():
            if not self.route_exists(key):
                self.app_paths[value.get("func")] = key
            type = value.get("type")
            if type == "page":
                self.page(key, *value.get("args"), **value.get("kwargs"))(value.get("func"))
            if type == "ui":
                self.ui(key, value["include_js"], value["include_css"])(value.get("func"))

    def return_funtion_response(self, response: Union[str, Response]) -> Union[str, Response]:
        Frame.get_stack().del_stack()
        return response

    def __ensure_request_response_signature__(self, func: Callable):
        data = {"request": Request, "response": Response}

        params = [p for p in inspect.signature(func).parameters.values()]
        for key, value in data.items():
            if key not in {p.name for p in params}:
                parm = inspect.Parameter(key, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=value)
                params.insert(0, parm)

        func.__signature__ = inspect.Signature(params)
