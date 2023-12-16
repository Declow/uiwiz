from typing import Literal
from uiwiz.element import Element


class Spinner(Element):
    _size: Literal["xs", "sm", "md", "lg"] = "sm"
    _type: Literal["spinner", "dots", "ring", "ball", "bars", "infinity"] = "ring"
    root_class: str = "loading "
    _classes: str = "loading-{0} loading-{1}"

    def __init__(self, spinner_for: Element = None) -> None:
        super().__init__("span")
        self.size = Spinner._size
        self.type = Spinner._type
        self.spinner_for = spinner_for
        self.__self__format()

    @property
    def spinner_for(self):
        return self._spinner_for

    @spinner_for.setter
    def spinner_for(self, element: Element) -> "Spinner":
        self._spinner_for = element
        if element:
            element.attributes["hx-indicator"] = f"#{self.id}"
            self.__self__format()

    def __self__format(self) -> None:
        clazz = Spinner._classes.format(self.type, self.size)
        if self.spinner_for:
            clazz += " htmx-indicator"
        self.classes(clazz)

    def extra_small(self) -> "Spinner":
        self.size = "xs"
        self.__self__format()
        return self

    def small(self) -> "Spinner":
        self.size = "sm"
        self.__self__format()
        return self

    def medium(self) -> "Spinner":
        self.size = "md"
        self.__self__format()
        return self

    def large(self) -> "Spinner":
        self.size = "lg"
        self.__self__format()
        return self

    def ring(self) -> "Spinner":
        self.type = "ring"
        self.__self__format()
        return self

    def spinner(self) -> "Spinner":
        self.type = "spinner"
        self.__self__format()
        return self

    def dots(self) -> "Spinner":
        self.type = "dots"
        self.__self__format()
        return self

    def ball(self) -> "Spinner":
        self.type = "ball"
        self.__self__format()
        return self

    def bars(self) -> "Spinner":
        self.type = "bars"
        self.__self__format()
        return self

    def infinity(self) -> "Spinner":
        self.type = "infinity"
        self.__self__format()
        return self
