from uiwiz.element import Element
from uiwiz import ui
from uiwiz.svg.svg_handler import get_svg, _type

class Toast(Element):
    _classes: str = "alert w-64"

    def __init__(self, message: str, svg: _type = None) -> None:
        super().__init__(tag="div", oob=True)
        self.attributes["id"] = f"toast"
        self.attributes["hx-swap-oob"] = "afterbegin"
        self._svg = svg
        with self:
            with Element().classes(Toast._classes) as toast_container:
                self.toast_container = toast_container
                if self._svg:
                    ui.html(get_svg(self._svg))
                Element("span", content=message)

    def svg(self, svg: _type) -> "Toast":
        self._svg = svg
        return self

    def classes(self, input: str) -> "Toast":
        self.toast_container.classes(input)
        return self
    
    def info(self) -> "Toast":
        self.classes(Toast._classes)
        self.__svg__("info")
        return self
    
    def warning(self) -> "Toast":
        self.classes(Toast._classes + " alert-warning")
        self.__svg__("warning")
        return self
    
    def success(self) -> "Toast":
        self.classes(Toast._classes + " alert-success")
        self.__svg__("success")
        return self
    
    def error(self) -> "Toast":
        self.classes(Toast._classes + " alert-error")
        self.__svg__("error")
        return self
    
    def __svg__(self, svg: _type):
        with self.toast_container:
            ui.html(get_svg(svg))
        self.toast_container.children.reverse()