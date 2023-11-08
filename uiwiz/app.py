import inspect
from pathlib import Path
from typing import Callable, Optional, Union
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from uiwiz.element import Element, Frame
import functools
import logging

logger = logging.getLogger("uiwiz")
logger.addHandler(logging.NullHandler())


class UiwizApp(FastAPI):
    page_routes = {}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        Frame.api = self.api
        self.templates = Jinja2Templates(Path(__file__).parent / 'templates')
        self.add_static_files('/static', Path(__file__).parent / 'static')

    def render(self, html_output: str, request: Request, status_code: int = 200):
        return self.templates.TemplateResponse("default.html",
            {
                'request': request,
                'root_element': [html_output],
            }, status_code, {'Cache-Control': 'no-store', 'X-uiwiz-Content': 'page'})
    
    def render_api(self, html_output: str, status_code: int = 200):
        return HTMLResponse(html_output, status_code, {'Cache-Control': 'no-store', 'X-uiwiz-Content': 'page'})
    
    def route_exists(self, path: str) -> None:
        return path in self.routes
    
    def remove_route(self, path: str) -> None:
        """Remove routes with the given path."""
        self.routes[:] = [r for r in self.routes if getattr(r, 'path', None) != path]

    def add_static_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        self.mount(url_path, StaticFiles(directory=str(local_directory)))

    def page(self, path: str, *args,
                 title: Optional[str] = None,
                 favicon: Optional[str] = None) -> Callable:
        def decorator(func: Callable, *args, **kwargs) -> Callable:
            self.remove_route(path)
            parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

            async def decorated(*dec_args, **dec_kwargs) -> Response:
                frame: Frame = Frame.get_stack()
                frame.app = self
                Element().classes("flex flex-col h-screen")
                request = dec_kwargs['request']
                # NOTE cleaning up the keyword args so the signature is consistent with "func" again
                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                result = func(*dec_args, **dec_kwargs)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                    return result
                html_output = frame.root_element.render()
                frame.del_stack()
                logger.debug(html_output)
                return self.render(html_output, request)

            parameters = [p for p in inspect.signature(func).parameters.values() if p.name != 'client']
            # NOTE adding request as a parameter so we can pass it to the client in the decorated function
            if 'request' not in {p.name for p in parameters}:
                parameters.append(inspect.Parameter('request', inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Request))
            decorated.__signature__ = inspect.Signature(parameters)

            self.page_routes[decorated] = path

            return self.get(path)(decorated)
        return decorator


    def api(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
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
                html_output = frame.root_element.render()
                frame.del_stack()
                logger.debug(html_output)
                return self.render_api(html_output)

            parameters = [p for p in inspect.signature(func).parameters.values() if p.name != 'client']
            if 'request' not in {p.name for p in parameters}:
                parameters.append(inspect.Parameter('request', inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Request))
            decorated.__signature__ = inspect.Signature(parameters)

            if not self.route_exists(path):
                self.page_routes[decorated] = path
            return self.post(path)(decorated)
        return decorator
