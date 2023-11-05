from fastapi import Request
from uiwis.element import Element
from functools import partial

class Label(Element):
    def __init__(self, text: str = "", for_: Element = None) -> None:
        super().__init__(tag="label")
        self.content = str(text)
        if for_:
            self.attributes["for"] = for_.id

    def set_text(self, text: str) -> "Label":
        self.content = text
        return self
    
    def bind_text_from(self, element: Element, attribute: str, trigger: str = "input delay:20ms"):
        async def bind_Value(request: Request):
            data = await request.json()
            l = Label(data[attribute])
            l.attributes["id"] = self.id
            
        element.events.append(
            {
                "target": f"#{self.id}",
                "func": bind_Value,
                "trigger": trigger,
            }
        )