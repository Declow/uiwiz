from pathlib import Path

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "swapy.min.js"
JS_PATH = Path(__file__).parent / "swapy.js"


class SwapyContainer(Element, extensions=[LIB_PATH, JS_PATH]):
    counter: int = 0
    item_counter: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.classes("space-y-4")

    def slot(self) -> Element:
        slot = Element()
        SwapyContainer.counter += 1
        slot.classes(f"section-{SwapyContainer.counter}")
        slot.attributes["data-swapy-slot"] = f"slot-{SwapyContainer.counter}"
        return slot

    def item(self) -> Element:
        item = Element()
        SwapyContainer.item_counter += 1
        item.classes(f"content-a bg-secondary")
        item.attributes["data-swapy-item"] = f"item-{SwapyContainer.item_counter}"
        return item
