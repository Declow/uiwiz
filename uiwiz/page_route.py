from typing import Any, Callable, List, Literal, TypedDict


class Path(TypedDict):
    func: Callable
    type: Literal["page", "ui"]
    args: Any
    kwargs: Any


class PageRouter:
    def __init__(self) -> None:
        self.paths: dict[str, Path] = {}

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

    def ui(self, path: str, *args, **kwargs) -> Callable:
        def setup(func):
            self.paths[path] = {"func": func, "type": "ui", "args": args, "kwargs": kwargs}
            return func

        return setup
