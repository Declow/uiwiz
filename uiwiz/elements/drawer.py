from uiwiz.element import Element
from uiwiz.elements.label import Label

class Drawer(Element):
    def __init__(self, left=True) -> None:
        super().__init__()
        with self.classes("drawer lg:drawer-open"):
            with Element().classes("drawer-side"):
                with Element("ul").classes("menu p-4 w-80 min-h-full bg-base-200 text-base-content"):
                    Element("li", content="asd")
