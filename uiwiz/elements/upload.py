from typing import Callable
from uiwiz.element import Element

class Upload(Element):
    _classes: str = "file-input file-input-bordered w-full max-w-xs"

    def __init__(self, on_upload: Callable, target: Callable, trigger: str = "change") -> None:
        super().__init__("input")
        self.attributes["type"] = "file"
        self.attributes["name"] = "file"
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