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
        """TextArea

        This element is used for text area inputs

        .. code-block:: python
            from uiwiz import ui

            ui.textarea("textarea", "Hello World", "Type something here"):

        :param name: name of the text area input
        :param value: default value of the text area input
        :param placeholder: placeholder of the text area input
        """
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
