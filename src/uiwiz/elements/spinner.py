from typing import Literal

from uiwiz.element import Element


class Spinner(Element):
    _size: Literal["xs", "sm", "md", "lg"] = "sm"
    _type: Literal["spinner", "dots", "ring", "ball", "bars", "infinity"] = "infinity"
    root_class: str = "loading "
    _classes: str = "loading-{0} loading-{1}"

    def __init__(self, *args: Element) -> None:
        """Spinner

        Show a spinner while making a request

        Example:
        .. code-block:: python
            from uiwiz import ui
            
            @app.ui("/some/endpoint")
            def some_endpoint():
                import time
                time.sleep(1)  # Simulate a long-running request
                ui.toast("Button clicked").success()

            with ui.button("Click me").on_click(some_endpoint, swap="none") as btn:
                ui.spinner(btn)

        :param args: Elements to show spinner for when making a request
        """
        super().__init__("span")
        self._size = Spinner._size
        self.type = Spinner._type
        self.spinner_for = args
        self.__self__format()

    @property
    def spinner_for(self):
        return self._spinner_for

    @spinner_for.setter
    def spinner_for(self, elements: tuple[Element]) -> "Spinner":
        self._spinner_for = elements
        if elements:
            for element in elements:
                element.attributes["hx-indicator"] = f"#{self.id}"
            self.__self__format()

    def __self__format(self) -> None:
        clazz = Spinner._classes.format(self.type, self._size)
        if self.spinner_for:
            clazz += " htmx-indicator"
        self.classes(clazz)

    def extra_small(self) -> "Spinner":
        self._size = "xs"
        self.__self__format()
        return self

    def small(self) -> "Spinner":
        self._size = "sm"
        self.__self__format()
        return self

    def medium(self) -> "Spinner":
        self._size = "md"
        self.__self__format()
        return self

    def large(self) -> "Spinner":
        self._size = "lg"
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
