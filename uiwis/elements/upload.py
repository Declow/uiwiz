from typing import Callable
from uiwis.element import Element

class Upload(Element):
    def __init__(self, on_upload: Callable, target: Callable, trigger: str = "change") -> None:
        super().__init__("input")
        self.attributes["type"] = "file"
        self.classes("file-input file-input-bordered w-full max-w-xs")
        self.attributes["name"] = "file"

        self.events.append({
            "func": on_upload,
            "inputs": None,
            "trigger": trigger,
            "endpoint": None,
            "target": target,
            "swap": "swap",
            "hx-encoding":'multipart/form-data'
        })