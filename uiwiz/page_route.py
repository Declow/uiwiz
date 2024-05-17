from typing import Callable, Optional


class PageRouter:
    def __init__(self) -> None:
        self.paths = {}

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
            self.paths[path] = {"func": func, "type": "page", "args": args, "kwargs": kwargs}
            return func

        return setup
