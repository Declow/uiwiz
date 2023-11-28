from typing import Optional
from fastapi import Request
from uiwiz.element import Element, Frame
import html

class Label(Element):
    def __init__(self, text: Optional[str] = None, for_: Element = None) -> None:
        super().__init__(tag="label")
        if text:
            self.content = text
        if for_:
            self.attributes["for"] = for_.id

    def set_text(self, text: str) -> "Label":
        self.content = text
        return self
    
    def bind_text_from(self, element: Element, trigger: str = "input delay:20ms"):
        """
        Remove attribute as it is not used but breaks bind for reasons
        """
        assert element.attributes.get("name") is not None

        async def bind_Value(request: Request):
            data = await request.json()
            self.set_frame_and_root()
            
            self.content = html.escape(data[element.attributes["name"]])
            

        element.event = {
                "target": f"#{self.id}",
                "func": bind_Value,
                "trigger": trigger,
            }