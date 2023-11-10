from fastapi import Request
from uiwiz.element import Element, Frame

class Label(Element):
    def __init__(self, text: str = "", for_: Element = None) -> None:
        super().__init__(tag="label")
        self.content = str(text)
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
            frame = Frame.get_stack()
            frame.root_element = self
            
            self.stack = frame
            self.content = data[element.attributes["name"]]
            

        element.events.append(
            {
                "target": f"#{self.id}",
                "func": bind_Value,
                "trigger": trigger,
            }
        )