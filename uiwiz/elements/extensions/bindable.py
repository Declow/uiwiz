import html
from fastapi import Request
from uiwiz.element import Element


class Bindable(Element):
    def bind_text_from(self, element: Element, trigger: str = "input delay:20ms", swap: str = "outerHTML"):
        """
        Remove attribute as it is not used but breaks bind for reasons
        """
        assert element.attributes.get("name") is not None

        async def bind_Value(request: Request):
            data = await request.json()
            self.set_frame_and_root()

            input_data = data[element.name]

            self.content = html.escape(str(input_data))

        element.event = {"target": f"#{self.id}", "func": bind_Value, "trigger": trigger, "swap": swap}

        return self
