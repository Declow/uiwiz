from fastapi import Request

from uiwiz.element import Element
from uiwiz.event import ON_EVENTS, SWAP_EVENTS


class Bindable(Element):
    def bind_text_from(
        self,
        element: Element,
        trigger: ON_EVENTS = "input delay:20ms",
        swap: SWAP_EVENTS = "outerHTML",
    ):
        """
        Bind the text of this element to data of another element.
        Requires the other element to have a name attribute.
        :param element: Element to bind to
        :param trigger: Event trigger to bind to
        """
        assert element.attributes.get("name") is not None

        async def bind_value(request: Request):
            data = await request.json()
            self.set_frame_and_root()

            input_data = data[element.name]

            self.content = str(input_data)

        bind_value.__name__ = f"{bind_value.__name__}_{element.id}"

        element.event = {
            "target": f"#{self.id}",
            "func": bind_value,
            "trigger": trigger,
            "swap": swap,
        }

        return self
