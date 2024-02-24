from fastapi import Request
from uiwiz.element import Element


class Bindable(Element):
    def bind_text_from(self, element: Element, trigger: str = "input delay:20ms", swap: str = "outerHTML"):
        """
        Remove attribute as it is not used but breaks bind for reasons
        """
        assert element.attributes.get("name") is not None

        async def bind_value(request: Request):
            data = await request.json()
            self.set_frame_and_root()

            input_data = data[element.name]

            self.content = str(input_data)

        bind_value.__hash__ = lambda: hash(element.id)

        element.event = {"target": f"#{self.id}", "func": bind_value, "trigger": trigger, "swap": swap}

        return self
