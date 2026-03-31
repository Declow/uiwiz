from fastapi import Request

from uiwiz.element import Element
from uiwiz.event import ON_EVENTS, SWAP_EVENTS


class Bindable(Element):
    def bind_text_from(
        self,
        element: Element,
        trigger: ON_EVENTS = "input delay:20ms",
        swap: SWAP_EVENTS = "outerHTML",
    ) -> "Bindable":
        """Bind the text of this element to data of another element.

        Requires the other element to have a name attribute.
        :param element: Element to bind to
        :type element: Element
        :param trigger: Event trigger to bind to
        :type trigger: ON_EVENTS, optional
        :param swap: Swap method to use
        :type swap: SWAP_EVENTS, optional
        :return: The bindable element
        :rtype: Bindable
        """
        if element.attributes.get("name") is None:
            raise ValueError("Element must have a name attribute to bind to")

        async def bind_value(request: Request) -> Bindable:
            data = await request.json()
            self._set_frame_and_root()

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
