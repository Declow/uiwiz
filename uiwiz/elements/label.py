from typing import Optional
from uiwiz.element import Element
from uiwiz.elements.extensions.bindable import Bindable


class Label(Bindable):
    def __init__(self, text: Optional[str] = None, for_: Element = None) -> None:
        super().__init__(tag="label")
        self.inline = True
        if text:
            self.content = text
        if for_:
            self.attributes["for"] = for_.id

    def set_text(self, text: str) -> "Label":
        self.content = text
        return self
