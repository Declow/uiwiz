from typing import Optional

from uiwiz.element import Element
from uiwiz.elements.checkbox import Checkbox
from uiwiz.elements.html import Html
from uiwiz.elements.label import Label
from uiwiz.svg.svg_handler import get_svg


class DrawerSetup(Element):
    _classes: str = "menu p-4 w-80 min-h-full bg-base-200 text-base-content"

    def __init__(self) -> None:
        super().__init__("ul")
        self.classes(DrawerSetup._classes)


class DrawerSide(Element):
    _classes: str = "drawer-side z-50"

    def __init__(self, drawer_toggle: Checkbox) -> None:
        super().__init__()
        self.classes(DrawerSide._classes)
        self.drawer_toggle = drawer_toggle

    def __enter__(self):
        super().__enter__()
        if not hasattr(self, "close_label"):
            self.close_label = Label("", self.drawer_toggle)
            self.close_label.attributes["class"] = "drawer-overlay"
            self.close_label.attributes["aria-label"] = "close sidebar"
        if not hasattr(self, "setup"):
            self.setup = DrawerSetup()
        self.setup.__enter__()

    def __exit__(self, *_):
        return super().__exit__(*_)


class DrawerContent(Element):
    _classes: str = "drawer-content flex flex-col min-h-screen"

    def __init__(self) -> None:
        super().__init__()
        self.classes(DrawerContent._classes)


class Drawer(Element):
    _classes: str = "drawer bg-base-100"

    def __init__(self, always_open: bool = False, right: bool = False) -> None:
        """Drawer

        A drawer is a panel that slides in from the side of the screen. It can be used to display additional content or controls.

        .. code-block:: python
            from uiwiz import ui

            with ui.drawer() as drawer:
                with drawer.drawer_content():
                    with ui.nav():
                        drawer.drawer_button()

                    with ui.col():
                        ui.label("test1")
                        ui.button("Click me")
                        ui.label("test1")

                with drawer.drawer_side():
                    with ui.element("li"):
                        ui.link("Drawer-1", "/")

        :param always_open: Always open the drawer until the screen size is too small.
        :type always_open: bool, optional
        :param right: Open the drawer from the right side of the screen.
        :type right: bool, optional
        """
        super().__init__()
        self.classes(Drawer._classes)
        self.__drawer_button_menu__: Optional[Element] = None

        self.always_open(always_open)
        self.right(right)

        with self:
            self.drawer_toggle = Checkbox("")
            self.drawer_toggle.attributes["class"] = "drawer-toggle"

    def drawer_content(self) -> Element:
        self._drawer_content = DrawerContent()
        return self._drawer_content

    def drawer_side(self) -> Element:
        self.side = DrawerSide(self.drawer_toggle)
        return self.side

    def drawer_button(self) -> Element:
        self.__drawer_button_menu__ = Element("label").classes("btn drawer-button")
        self.__drawer_button_menu__.attributes["for"] = self.drawer_toggle.id
        with self.__drawer_button_menu__:
            Html(get_svg("menu"))

    def always_open(self, value: bool) -> None:
        """Set the drawer to always open until the screen size is too small."""
        if value:
            self.classes(self.attributes["class"] + " lg:drawer-open")
        else:
            self.classes(self.attributes["class"].replace("lg:drawer-open", ""))

    def right(self, value: bool) -> None:
        """Set the drawer to open from the right side of the screen."""
        if value:
            self.classes(self.attributes["class"] + " drawer-end")
        else:
            self.classes(self.attributes["class"].replace("drawer-end", ""))
