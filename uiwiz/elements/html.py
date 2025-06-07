from uiwiz.element import Element


class Html(Element):
    def __init__(self, content) -> None:
        """Html element

        Will render a raw htlm string. This is useful for embedding custom HTML content directly into the UI.

        .. code-block:: python
            from uiwiz import ui

            ui.html("<strong>Hello World</strong>")

        :param content: html content as string
        :type content: str
        """
        super().__init__()
        self.__content__ = content

    @property
    def content(self) -> str:
        return self.__content__

    @content.setter
    def content(self, content):
        self.__content__ = content
