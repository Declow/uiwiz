from uiwiz.element import Element
from uiwiz.elements.checkbox import Checkbox
from uiwiz.elements.label import Label


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
        close_label = Label("", self.drawer_toggle)
        close_label.attributes["class"] = "drawer-overlay"
        close_label.attributes["aria-label"] = "close sidebar"
        self.setup = DrawerSetup()
        self.setup.__enter__()

    def __exit__(self, *_):
        return super().__exit__(*_)


class DrawerContent(Element):
    _classes: str = "drawer-content flex flex-col"

    def __init__(self) -> None:
        super().__init__()
        self.classes(DrawerContent._classes)


class Drawer(Element):
    _classes: str = "drawer bg-base-100 min-h-screen h-full"

    def __init__(self, always_open: bool = False, right: bool = False) -> None:
        super().__init__()
        self.classes(Drawer._classes)

        if always_open:
            self.classes(self.attributes["class"] + " lg:drawer-open")
        if right:
            self.classes(self.attributes["class"] + " drawer-end")

        with self:
            self.drawer_toggle = Checkbox("").classes("drawer-toggle")

    def drawer_content(self) -> Element:
        self.drawer_content = DrawerContent()
        return self.drawer_content

    def drawer_side(self) -> Element:
        self.side = DrawerSide(self.drawer_toggle)
        return self.side
