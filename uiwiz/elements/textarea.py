from typing import Optional

from uiwiz.elements.extensions.on_event import OnEvent


class TextArea(OnEvent):
    root_class: str = "textarea "
    root_size: str = "textarea-{size}"
    _classes: str = "textarea-bordered w-full"

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        placeholder: Optional[str] = None,
    ) -> None:
        super().__init__("textarea")
        self.attributes["name"] = name
        if placeholder:
            self.placeholder = placeholder
        if value:
            self.content = value
        self.classes(TextArea._classes)
        self.size(self._size)

    @property
    def placeholder(self) -> Optional[str]:
        return self.attributes["placeholder"]

    @placeholder.setter
    def placeholder(self, value: str):
        self.attributes["placeholder"] = value
        return self
