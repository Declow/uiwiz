import functools
import inspect
from html import escape
from typing import Any, Callable, Literal, Optional, TypedDict, Union

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from jinja2 import Template

from uiwiz.asgi_request_middelware import get_request
from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.shared import register_path, route_exists
from uiwiz.version import __version__


class PathDefinition(TypedDict):
    func: Callable
    type: Literal["page", "ui"]
    args: Any
    kwargs: Any
    include_js: bool
    include_css: bool


class PageRouter:
    def __init__(self) -> None:
        self.paths: dict[str, PathDefinition] = {}

    def page(
        self,
        path: str,
        *args,
        **kwargs,
    ) -> Callable:
        def setup(func):
            self.paths[path] = {"func": func, "type": "page", "args": args, "kwargs": kwargs}
            return func

        return setup

    def ui(self, path: str, include_js: bool = True, include_css: bool = True, *args, **kwargs) -> Callable:
        def setup(func):
            self.paths[path] = {
                "func": func,
                "type": "ui",
                "args": args,
                "kwargs": kwargs,
                "include_js": include_js,
                "include_css": include_css,
            }
            return func

        return setup


class PageRouterV2(APIRouter):
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
        app = get_request().app

        theme = app.theme
        if cookie_theme := request.cookies.get("data-theme"):
            theme = f"data-theme={escape(cookie_theme)}"

        root_overflow = f'style="{root_overflow}"'
        standard_headers = {"cache-control": "no-store", "x-uiwiz-content": "page"}
        default_page: Template = app.templates.get_template(template_name)

        if response:
            for key, value in response.headers.items():
                standard_headers[key] = value

        return self.return_funtion_response(
            HTMLResponse(
                content=default_page.render(
                    request=request,
                    root_element=[frame.render()],
                    title=app.__get_title__(frame, title),
                    theme=theme,
                    ext_js=ext_js,
                    ext_css=ext_css,
                    toast_delay=app.toast_delay,
                    error_classes=app.error_classes,
                    auth_header_name=app.auth_header,
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

    def page(self, path: str, *args, title: Optional[str] = None, favicon: Optional[str] = None, **kwargs) -> Callable:
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

            if not route_exists(path):
                register_path(path, decorated)

            return self.get(path, *args, include_in_schema=False, **kwargs)(decorated)

        return decorator

    def ui(self, path: str, include_js: bool = True, include_css: bool = True, **kwargs) -> Callable:
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

            if not route_exists(path):
                register_path(path, decorated)

            return self.post(path, include_in_schema=False, **kwargs)(decorated)

        return decorator

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
