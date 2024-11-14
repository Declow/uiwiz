from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import FUNC_TYPE, ON_EVENTS, SWAP_EVENTS, TARGET_TYPE


class Upload(OnEvent):
    root_class: str = "file-input "
    root_size: str = "file-input-{size}"
    _classes: str = "file-input-bordered"

    def __init__(
        self,
        name: str,
    ) -> "Upload":
        super().__init__("input")
        self.attributes["type"] = "file"
        self.attributes["name"] = name
        self._size = "sm"
        self.classes(Upload._classes)

    def on_upload(
        self,
        on_upload: FUNC_TYPE,
        target: TARGET_TYPE = None,
        trigger: ON_EVENTS = "change",
        swap: SWAP_EVENTS = None,
    ) -> "Upload":
        self.event = {
            "func": on_upload,
            "trigger": trigger,
            "target": target,
            "swap": swap,
            "hx-encoding": "multipart/form-data",
        }

        return self
