import functools
import inspect
from typing import Callable, Optional, Union

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from uiwiz.asgi_request_middelware import get_request
from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.shared import register_path, route_exists
from uiwiz.version import __version__


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

                _app = get_request().app
                return _app.render(request, response, title)

            self.__ensure_request_response_signature__(decorated)

            _router = router or self
            full_path = _router.prefix + path

            if not route_exists(full_path):
                register_path(full_path, decorated)

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

            _router = router or self
            full_path = _router.prefix + path

            if not route_exists(full_path):
                register_path(full_path, decorated)

            return _router.post(path, include_in_schema=False, **kwargs)(decorated)

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
