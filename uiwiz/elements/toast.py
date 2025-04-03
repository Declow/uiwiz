import json
from typing import Optional

from uiwiz import ui
from uiwiz.element import Element
from uiwiz.svg.svg_handler import _type, get_svg


class Toast(Element):
    root_class: str = "alert w-full z-50 "

    def __init__(self, message: str = "", svg: _type = None) -> None:
        """Toast

        Display a toast message on the client side.
        Can be used anywhere in a @page_router.ui("<path>") or @app.ui("<path>")

        .. code-block:: python
            @app.ui("/some/path")
            async def some_path():
                ui.toast("This is a toast message").info()

        To persist the toast message, set auto_close to False

        .. code-block:: python
            @app.ui("/some/path")
            async def some_path():
                ui.toast("This is a toast message").info().set_auto_close(False)

        :param message: The message to display
        :param svg: The svg to display. One of "info", "warning", "success", "error", "menu"

        """
        self.inner_class = Toast.root_class
        super().__init__(tag="div", oob=True)
        self.attributes["id"] = "toast"
        self.attributes["hx-swap-oob"] = "afterbegin"
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

    def set_auto_close(self, auto_close: bool) -> "Toast":
        """Set auto close

        :param auto_close: True or False. Auto close False will keep the toast open until the user closes it
        """
        self.auto_close = auto_close
        return self

    def before_render(self):
        with self:
            with self.inner_element.classes(self.inner_class + " relative pr-16"):
                if self._svg:
                    svg = ui.html(get_svg(self._svg))
                    self.inner_element.children.remove(svg)
                    self.inner_element.children.insert(0, svg)
                Element("span", content=self.message)
                self.inner_element.attributes["hx-toast-data"] = json.dumps({"autoClose": self._auto_close})
                btn = None
                self.inner_element.attributes["hx-toast-delete-button"] = lambda: btn.id if btn else ""
                if not self._auto_close:
                    btn = ui.button("✕").classes("btn btn-sm btn-circle btn-ghost absolute right-2 top")

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
