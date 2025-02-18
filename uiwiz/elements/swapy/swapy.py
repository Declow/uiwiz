from pathlib import Path

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "swapy.min.js"
JS_PATH = Path(__file__).parent / "swapy.js"
CSS_PATH = Path(__file__).parent / "swapy.css"


class SwapyContainer(Element, extensions=[LIB_PATH, JS_PATH, CSS_PATH]):
    counter: int = 0
    item_counter: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.classes("space-y-4")

        Element(content="test").classes("my-button")

    def slot(self, slot_name=None) -> Element:
        slot = Element()
        SwapyContainer.counter += 1
        slot.classes(f"slot")
        slot.attributes["data-swapy-slot"] = f"slot-{SwapyContainer.counter}" if slot_name is None else slot_name
        return slot

    def item(self) -> Element:
        item = Element()
        SwapyContainer.item_counter += 1
        item.classes(f"content-a bg-secondary")
        item.attributes["data-swapy-item"] = f"item-{SwapyContainer.item_counter}"
        return item
