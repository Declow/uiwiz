from typing import Callable, Union

from uiwiz.element import Element


class Link(Element):
    root_class: str = "link "
    _classes: str = "link-hover"

    def __init__(self, text: str, link: Union[Callable[[], str], str]) -> None:
        """Link element

        Link element that can be used to navigate to a different page.
        Can be used as a button or a link.

        Example:
        .. code-block:: python
        
            from uiwiz import ui

            ui.link("Click me", "/some/path").classes("btn btn-primary") 

        :param text: The text to display
        :type text: str
        :param link: The link to navigate to when clicked. Can be a callable that returns a string
        :type link: Union[Callable[[], str], str]
        """
        super().__init__("a")
        self.content = text
        self.link = link
        if isinstance(link, str):
            self.attributes["href"] = link
        self.classes(Link._classes)

    def before_render(self) -> None:
        if callable(self.link):
            self.attributes["href"] = self.link()
            return
        self.attributes["href"] = self.link
