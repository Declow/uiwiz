from typing import Callable, Optional


class PageRouter:
    def __init__(self) -> None:
        self.paths = {}

    def page(
        self,
        path: str,
        *args,
        title: Optional[str] = "uiwiz",
        favicon: Optional[str] = None,
    ) -> Callable:
        def setup(func, *args, **kwargs):
            self.paths[path] = {"func": func, "type": "page"}
            return func

        return setup

    def ui(self, path: str) -> Callable:
        def setup(func, *args, **kwargs):
            self.paths[path] = {"func": func, "type": "ui"}
            return func

        return setup
