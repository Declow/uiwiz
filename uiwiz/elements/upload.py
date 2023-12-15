from typing import Callable
from uiwiz.element import Element

class Upload(Element):
    root_class: str = "file-input "
    _classes: str = "file-input-bordered w-full max-w-xs"

    def __init__(self, name: str, on_upload: Callable, target: Callable, trigger: str = "change") -> None:
        super().__init__("input")
        self.attributes["type"] = "file"
        self.attributes["name"] = name
        self.classes(Upload._classes)

        self.event = {
            "func": on_upload,
            "inputs": None,
            "trigger": trigger,
            "endpoint": None,
            "target": target,
            "swap": "swap",
            "hx-encoding":'multipart/form-data'
        }