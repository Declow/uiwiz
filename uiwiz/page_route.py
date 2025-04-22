import functools
import inspect
import json
from dataclasses import dataclass
from html import escape
from typing import Callable, Optional, Union

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.version import __version__


@dataclass
class Page:
    header: Element
    body: Element
    content: Element


class PageRouter(APIRouter):
    def page(
        self,
        path: str,
        *args,
        title: Optional[str] = None,
        favicon: Optional[str] = None,
        router: Optional[APIRouter] = None,
        **kwargs,
    ) -> Callable:
        def decorator(func: Callable, *args, **kwargs) -> Callable:
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                Frame.get_stack().del_stack()
                # Create frame before function is called

                request = dec_kwargs["request"]
                response = dec_kwargs["response"]

                # NOTE Ensure the signature matches the parameters of the function

                page = self.render(request, title=title)
                with page.content:
                    dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                    result = func(*dec_args, **dec_kwargs)
                    if inspect.isawaitable(result):
                        result = await result

                if isinstance(result, Response):
                    return self.return_function_response(result)
                standard_headers = {"cache-control": "no-store", "x-uiwiz-content": "page"}

                if response:
                    standard_headers.update(response.headers)

                self.add_ext(page, include_js=True, include_css=True)

                return HTMLResponse(
                    content=Frame.get_stack().render(),
                    status_code=200,
                    media_type="text/html",
                )

            self.__ensure_request_response_signature__(decorated)

            _router = router or self

            return _router.get(path, *args, include_in_schema=False, **kwargs)(decorated)

        return decorator

    def ui(
        self,
        path: str,
        include_js: bool = True,
        include_css: bool = True,
        router: Optional[APIRouter] = None,
        **kwargs,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            # Capture values at decoration time
            cap_include_js = include_js
            cap_include_css = include_css
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs) -> Response:
                Frame.get_stack().del_stack()
                Frame.get_stack()  # Create frame before function is called
                response = dec_kwargs["response"]

                # Ensure the signature matches the parameters of the function
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result

                if isinstance(result, Response):
                    return self.return_function_response(result)

                standard_headers = {"cache-control": "no-store", "x-uiwiz-content": "partial-ui"}
                standard_headers.update(response.headers)

                self.add_ext(page=None, include_js=cap_include_js, include_css=cap_include_css)

                content = Frame.get_stack().render()
                return self.return_function_response(HTMLResponse(content=content, headers=standard_headers))

            self.__ensure_request_response_signature__(decorated)
            _router = router or self
            return _router.post(path, include_in_schema=False, **kwargs)(decorated)

        return decorator

    def return_function_response(self, response: Union[str, Response]) -> Union[str, Response]:
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

    def add_ext(self, page: Optional["Page"] = None, include_js: bool = False, include_css: bool = False) -> None:
        lib_css = []
        for lib in Frame.get_stack().extensions:
            if lib.endswith("css") and include_css:
                lib_css.append(lib)
                if page is None:
                    Element("link", href=lib, rel="stylesheet", type="text/css")
                else:
                    with page.header:
                        Element("link", href=lib, rel="stylesheet", type="text/css")

                    # Hack to make aggrid work with daisyui
                    with page.body:
                        Element("link", href=lib, rel="stylesheet", type="text/css")
            elif lib.endswith("js") and include_js:
                if page is None:
                    Element("script", src=lib)
                else:
                    with page.body:
                        Element("script", src=lib)
            if not lib.endswith("js") and not lib.endswith("css"):
                raise Exception("lib type not supported, supported types css, js")

    def render(
        self,
        request: Request,
        title: Optional[str],
        html_classes: str = "overflow-y-scroll",
        lang: str = "en",
    ) -> Page:
        frame = Frame.get_stack()

        theme = request.app.theme
        if cookie_theme := request.cookies.get("data-theme"):
            theme = escape(cookie_theme)

        class RenderDoctype:
            def render(self):
                return "<!DOCTYPE html>"

        Frame.get_stack().root = [RenderDoctype()]  # funky way to add doctype
        with Element("html").classes(html_classes) as html:
            html.attributes["id"] = "html"
            html.attributes["lang"] = lang
            html.attributes["data-theme"] = theme

            with Element("head") as header:
                Element("meta", name="viewport").attributes["content"] = "width=device-width, initial-scale=1"
                Element("meta", charset="utf-8")
                Element("meta", description=frame.meta_description_content)

                Element("title", content=request.app.__get_title__(frame, title))

                Element("link", href=f"/_static/{__version__}/libs/daisyui.css", rel="stylesheet", type="text/css")
                Element(
                    "link", href=f"/_static/{__version__}/libs/daisyui-themes.css", rel="stylesheet", type="text/css"
                )
                Element("script", src=f"/_static/{__version__}/libs/tailwind.js")
                Element("link", href=f"/_static/{__version__}/app.css", rel="stylesheet", type="text/css")
            with Element("body") as body:
                body.attributes["hx-ext"] = "swap-header"
                with Element("div", id="content"):
                    with Element().classes("flex flex-col min-h-screen h-full") as content:
                        pass

                toast = Element("div").classes("toast toast-top toast-end text-wrap z-50")
                toast.attributes["id"] = "toast"
                toast.attributes["hx-toast-delay"] = json.dumps({"delay": request.app.toast_delay})

                Element("script", src=f"/_static/{__version__}/libs/htmx1.9.9.min.js")
                Element("script", src=f"/_static/{__version__}/libs/htmx-json-enc.js")
                Element("script", src=f"/_static/{__version__}/default.js")
        return Page(header=header, body=body, content=content)
