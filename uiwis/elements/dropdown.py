from uiwis.element import Element

class Dropdown(Element):
    def __init__(self, items: list[str], placeholder: str = None) -> None:
        super().__init__("select")
        self.classes("select select-bordered w-full max-w-xs")
        with self:
            if placeholder:
                Element("option disabled selected", content=placeholder)
            for item in items:
                Element("option", content=item)
        