from typing import Optional

from uiwiz.element import Element
from uiwiz.event import FUNC_TYPE, ON_EVENTS, SWAP_EVENTS, TARGET_TYPE


class OnEvent(Element):
    def on(
        self,
        trigger: ON_EVENTS,
        func: FUNC_TYPE,
        target: TARGET_TYPE = None,
        swap: SWAP_EVENTS = None,
        params: Optional[dict[str, str]] = None,
    ) -> "OnEvent":
        """
        Register the type of event to listen for and the function to call when the event is triggered.

        :param trigger: The type of event to listen for. This can be any valid html event type.
        :param func: The function/endpoint to call when the event is triggered.
        :param target: The target element that will be swaped with the response from the server.
        :param swap: The type of swap to perform. Set to 'none' to disable swapping.
        :param params: The parameters to pass to the function/endpoint. This could be a dynamic value that the function needs to execute. /some/path/{id}

        :return: The current instance of the element.
        """
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
