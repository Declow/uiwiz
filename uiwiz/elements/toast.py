from uiwiz.element import Element
from uiwiz import ui
from uiwiz.svg.svg_handler import get_svg, _type


class Toast(Element):
    root_class: str = "alert w-full z-50 "

    def __init__(self, message: str = "", svg: _type = None) -> None:
        super().__init__(tag="div", oob=True)
        self.attributes["id"] = "toast"
        self.attributes["hx-swap-oob"] = "afterbegin"
        self._svg = svg
        self.message = message
        self.context_manager_used = False
        self.inner_element = None
        self.inner_class = Toast.root_class

    def before_render(self):
        with self:
            with self.inner_element.classes(self.inner_class):
                if self._svg:
                    svg = ui.html(get_svg(self._svg))
                    self.inner_element.children.remove(svg)
                    self.inner_element.children.insert(0, svg)
                Element("span", content=self.message).inline = True

    def __enter__(self):
        super().__enter__()
        if self.inner_element is None:
            self.inner_element = Element().classes(self.inner_class)
        self.inner_element.__enter__()
        return self

    def svg(self, svg: _type) -> "Toast":
        self._svg = svg
        return self

    def classes(self, input: str) -> "Toast":
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
        return self
