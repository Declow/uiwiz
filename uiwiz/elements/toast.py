import json
from typing import Optional

from uiwiz import ui
from uiwiz.element import Element
from uiwiz.svg.svg_handler import _type, get_svg


class Toast(Element):
    root_class: str = "alert w-full z-50 "

    def __init__(self, message: str = "", svg: _type = None) -> None:
        self.inner_class = Toast.root_class
        super().__init__(tag="div", oob=True)
        self.attributes["id"] = "toast"
        self.attributes["hx-swap-oob"] = "afterbegin"
        self.attributes["hx-toast-auto-close"] = "true"
        self._svg: _type = svg
        self.message: str = message
        self.context_manager_used: bool = False
        self.inner_element: Optional[Element] = None
        self._auto_close: bool = True

    @property
    def auto_close(self) -> bool:
        return self._auto_close
    
    @auto_close.setter
    def auto_close(self, auto_close: bool) -> None:
        self._auto_close = auto_close
        self.attributes["hx-toast-auto-close"] = str(auto_close).lower()

    def before_render(self):
        with self:
            with self.inner_element.classes(self.inner_class):
                if self._svg:
                    svg = ui.html(get_svg(self._svg))
                    self.inner_element.children.remove(svg)
                    self.inner_element.children.insert(0, svg)
                message = Element("span", content=self.message)
                message.attributes["hx-toast-data"] = json.dumps({"autoClose": self._auto_close})
                btn = None
                message.attributes["hx-toast-delete-button"] = lambda: btn.id if btn else ""
                if not self._auto_close:
                    btn = ui.button("✕").classes("btn btn-sm btn-circle btn-ghost absolute right-2 top-2")

    def __enter__(self):
        super().__enter__()
        if self.inner_element is None:
            self.inner_element = Element().classes(self.inner_class)
        self.inner_element.__enter__()
        return self

    def svg(self, svg: _type) -> "Toast":
        self._svg = svg
        return self

    def classes(self, input: str = "") -> "Toast":
        self.inner_class = self.inner_class + input
        return self

    def info(self) -> "Toast":
        self.classes("alert")
        self.svg("info")
        return self

    def warning(self) -> "Toast":
        self.classes("alert-warning")
        self.svg("warning")
        return self

    def success(self) -> "Toast":
        self.classes("alert-success")
        self.svg("success")
        return self

    def error(self) -> "Toast":
        self.classes("alert-error")
        self.svg("error")
        self.auto_close = False
        return self