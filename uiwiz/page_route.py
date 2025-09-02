import functools
import inspect
from functools import partial
from typing import Annotated, Any, Callable, Optional, Sequence, Type, TypedDict

from fastapi import APIRouter, Request, Response, params
from fastapi.datastructures import Default
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRoute
from starlette.types import ASGIApp, Lifespan
from typing_extensions import Doc

from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.page_definition import PageDefinition


class DecKwargs(TypedDict):
    page: PageDefinition
    request: Request
    response: Response


class PageRouter(APIRouter):
    """
    `PageRouter` class, used to group *path operations*, for example to structure
    an app in multiple files. It would then be included in the `UiWizard` app, or
    in another `PageRouter` (ultimately included in the app).

    ## Example

    ```python
    from uiwiz import PageRouter, UiwizApp, ui

    app = UiwizApp()
    router = PageRouter()

    @router.get("/users/", tags=["users"])
    async def read_users():
        ui.element("h1", content="Hello world")

    app.include_router(router)
    ```
    """

    def __init__(
        self,
        *,
        prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
        dependencies: Annotated[
            Optional[Sequence[params.Depends]],
            Doc(
                """
                A list of dependencies (using `Depends()`) to be applied to all the
                *path operations* in this router.

                Read more about it in the
                [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                """
            ),
        ] = None,
        default_response_class: Annotated[
            Type[Response],
            Doc(
                """
                The default response class to be used.

                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).
                """
            ),
        ] = Default(JSONResponse),
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.
                """
            ),
        ] = True,
        default: Annotated[
            Optional[ASGIApp],
            Doc(
                """
                Default function handler for this router. Used to handle
                404 Not Found errors.
                """
            ),
        ] = None,
        route_class: Annotated[
            Type[APIRoute],
            Doc(
                """
                Custom route (*path operation*) class to be used by this router.

                Read more about it in the
                [FastAPI docs for Custom Request and APIRoute class](https://fastapi.tiangolo.com/how-to/custom-request-and-route/#custom-apiroute-class-in-a-router).
                """
            ),
        ] = APIRoute,
        # which the router cannot know statically, so we use typing.Any
        lifespan: Annotated[
            Optional[Lifespan[Any]],
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        page_definition_class: Annotated[
            Optional[Type[PageDefinition]],
            Doc("""
                The page definition class to use for this router.
                
                This enables the use of custom page definitions for rendering the HTML
                pages. The default is `PageDefinition`, which provides a basic HTML
                structure. You can create your own class that inherits from `PageDefinition`
                and override the `header`, `body`, and `content` methods to customize the
                HTML structure and content as needed. Setting the `page_definition_class` in the 
                UiwizApp will set the default for all routers.
                Example:
                ```python
                class MyPageDefinition(PageDefinition):
                    def header(self, header: Element) -> None:
                        # Custom header content
                        Element("link", href="/custom.css", rel="stylesheet")
                
                    def body(self, body: Element) -> None:
                        # Custom body content
                        Element("div", content="Custom Body").classes("custom-body")
                
                    def content(self, content: Element) -> None:
                        # Custom content
                        Element("h1", content="Custom Content").classes("custom-content")
                """),
        ] = None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            dependencies=dependencies,
            default_response_class=default_response_class,
            redirect_slashes=redirect_slashes,
            default=default,
            route_class=route_class,
            lifespan=lifespan,
            **kwargs,
        )
        if page_definition_class is not None and not issubclass(page_definition_class, PageDefinition):
            raise TypeError("page_definition_class must be a subclass of PageDefinition")
        self.page_definition_class = page_definition_class

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
            cap_title = title

            @functools.wraps(func)
            async def decorated(*dec_args, **dec_kwargs: DecKwargs) -> Response:
                Frame.get_stack().del_stack()
                # Create frame before function is called

                request = dec_kwargs["request"]
                response = dec_kwargs["response"]

                if self.page_definition_class is None:
                    self.page_definition_class = request.app.page_definition_class

                # NOTE Ensure the signature matches the parameters of the function
                page: PageDefinition = dec_kwargs.get("page") if "page" in dec_kwargs else self.page_definition_class()

                dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
                user_method = partial(func, *dec_args, **dec_kwargs)
                result = await page.render(user_method=user_method, request=request, title=cap_title)
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
        include_js: bool = False,
        include_css: bool = False,
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
                    Frame.get_stack().del_stack()
                    return result

                standard_headers = {"cache-control": "no-store", "x-uiwiz-content": "partial-ui"}
                standard_headers.update(response.headers)

                self.add_ext(page=None, include_js=cap_include_js, include_css=cap_include_css)

                content = Frame.get_stack().render()
                return HTMLResponse(content=content, headers=standard_headers)

            self.__ensure_request_response_signature__(decorated)
            _router = router or self
            return _router.post(path, include_in_schema=False, **kwargs)(decorated)

        return decorator

    def __ensure_request_response_signature__(self, func: Callable):
        data = {"request": Request, "response": Response}

        params = [p for p in inspect.signature(func).parameters.values()]
        for key, value in data.items():
            if key not in {p.name for p in params}:
                parm = inspect.Parameter(key, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=value)
                params.insert(0, parm)

        func.__signature__ = inspect.Signature(params)

    def add_ext(
        self,
        page: Optional["PageDefinition"] = None,
        include_js: bool = False,
        include_css: bool = False,
    ) -> None:
        lib_css = []
        for lib in Frame.get_stack().extensions:
            if lib.endswith("css") and include_css:
                lib_css.append(lib)
                if page is None:
                    Element("link", href=lib, rel="stylesheet", type="text/css")
                else:
                    with page.header_ele:
                        Element("link", href=lib, rel="stylesheet", type="text/css")

                    # Hack to make aggrid work with daisyui
                    with page.html_ele:
                        Element("link", href=lib, rel="stylesheet", type="text/css")
            elif lib.endswith("js") and include_js:
                if page is None:
                    Element("script", src=lib, type="module")
                else:
                    with page.html_ele:
                        Element("script", src=lib, type="module")
            if not lib.endswith("js") and not lib.endswith("css"):
                raise Exception("lib type not supported, supported types css, js")
