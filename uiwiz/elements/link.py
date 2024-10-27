from typing import Callable, Union

from uiwiz.element import Element


class Link(Element):
    root_class: str = "link "
    _classes: str = "link-hover"

    def __init__(self, text: str, link: Union[Callable[[], str], str]) -> None:
        super().__init__("a")
        self.content = text
        self.link = link
        if isinstance(link, str):
            self.attributes["href"] = link
        self.classes(Link._classes)

    def before_render(self):
        if callable(self.link):
            self.attributes["href"] = self.link()
            return
        self.attributes["href"] = self.link
