from typing import Callable, Union
from uiwiz.element import Element


class Upload(Element):
    root_class: str = "file-input "
    _classes: str = "file-input-bordered file-input-sm"

    def __init__(
        self,
        name: str,
        on_upload: Callable,
        target: Union[Callable, str, Element] = None,
        trigger: str = "change",
        swap: str = None,
    ) -> "Upload":
        super().__init__("input")
        self.attributes["type"] = "file"
        self.attributes["name"] = name
        self.classes(Upload._classes)

        self.event = {
            "func": on_upload,
            "trigger": trigger,
            "target": target,
            "swap": swap,
            "hx-encoding": "multipart/form-data",
        }
