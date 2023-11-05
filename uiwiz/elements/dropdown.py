from uiwiz.element import Element

class Dropdown(Element):
    _classes: str = "select select-bordered w-full max-w-xs"

    def __init__(self, items: list[str], placeholder: str = None) -> None:
        super().__init__("select")
        self.classes(Dropdown._classes)
        with self:
            if placeholder:
                Element("option disabled selected", content=placeholder)
            for item in items:
                Element("option", content=item)
        