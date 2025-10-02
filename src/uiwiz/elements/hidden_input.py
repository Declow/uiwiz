from typing import Any, Optional

from uiwiz.element import Element


class HiddenInput(Element):
    _classes: str = ""

    def __init__(
        self,
        name: str,
        value: Optional[Any] = None,
    ) -> None:
        """HiddenInput

        This element is used for hidden input data that should not be visible to the user.
        But it will be sent back to the server when the form is submitted.

        Example:
        .. code-block:: python

            from uiwiz import ui
            from pydantic import BaseModel

            class HiddenInputExample(BaseModel):
                csrf_token: str
                age: int
                

            @app.ui("/ui/hiddeninput/submit")
            async def ui_hiddeninput_submit(data_input: HiddenInputExample):
                with ui.toast().set_auto_close(False).success():
                    ui.dict(data_input.dict()).border_classes("")

            with ui.form().on_submit(ui_hiddeninput_submit):
                ui.hiddenInput(name="csrf_token", value="hidden_csrf_token")
                ui.input("age", None, "Enter your age")
                ui.button("Submit")

        :param name: Used in the attributes name sent back in json
        :type name: str
        :param value: The value to send back
        :type value: Any
        """
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["value"] = value
        self.attributes["type"] = "hidden"
