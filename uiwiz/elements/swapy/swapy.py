from pathlib import Path
from typing import Optional, TypedDict

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "swapy.min.js"
JS_PATH = Path(__file__).parent / "swapy.js"


class Config(TypedDict):
    drag_axis: str
    drag_on_hold: bool
    auto_scroll_on_drag: bool
    swap_mode: str
    animation: str
    enabled: bool


class SwapyContainer(Element, extensions=[LIB_PATH, JS_PATH]):
    counter: int = 0
    item_counter: int = 0

    def __init__(self, config: Optional[Config]) -> None:
        super().__init__()
        self.classes("space-y-4")
        if config is None:
            config = {}
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary")
        
        attributes = {
            "data-wiz-animation": config.get("animation", "dynamic"),
            "data-wiz-swap-mode": config.get("swap_mode", "drop"),
            "data-wiz-auto-scroll-on-drag": config.get("auto_scroll_on_drag", "true"),
            "data-wiz-enabled": config.get("enabled", "true"),
            "data-wiz-drag-axis": config.get("drag_axis", "x"),
            "data-wiz-drag-on-hold": config.get("drag_on_hold", "false"),
        }
        self.attributes.update(attributes)

        Element(content="test").classes("my-button")

    def slot(self, slot_name=None) -> Element:
        slot = Element()
        SwapyContainer.counter += 1
        slot.classes(f"section-{SwapyContainer.counter}")
        slot.attributes["data-swapy-slot"] = f"slot-{SwapyContainer.counter}" if slot_name is None else slot_name
        return slot

    def item(self) -> Element:
        item = Element()
        SwapyContainer.item_counter += 1
        item.classes(f"content-a bg-secondary")
        item.attributes["data-swapy-item"] = f"item-{SwapyContainer.item_counter}"
        return item
