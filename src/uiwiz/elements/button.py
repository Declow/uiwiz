from typing import Optional

from uiwiz import ui
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import FUNC_TYPE, SWAP_EVENTS, TARGET_TYPE


def some_function():
    ui.toast("Button clicked").success()


class Button(OnEvent):
    root_class: str = "btn"
    root_size: str = "btn-{size}"

    def __init__(self, title: str) -> None:
        """
        Create a button element, with the given title.
        Can be used to trigger events.

        Example:
        .. code-block:: python

            from uiwiz import ui

            @app.ui("/ui/toast/click")
            def click_event():
                ui.toast("Button clicked").success()

            ui.button("Click me").on_click(click_event, target="this", swap="none")

        :param title: The title of the button
        :type title: str
        """
        super().__init__(tag="button")
        self.content = title

    def on_click(
        self,
        func: FUNC_TYPE = None,
        target: TARGET_TYPE = None,
        swap: SWAP_EVENTS = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Button":
        self.event = {"func": func, "trigger": "click", "target": target, "swap": swap, "params": params}
        return self
