from typing import Any, Callable, List, Literal, TypedDict


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
