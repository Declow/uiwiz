from uiwiz.element import Element


class Dropdown(Element):
    root_class: str = "select "
    _classes: str = "select-bordered w-full max-w-xs"

    def __init__(self, name: str, items: list[str], placeholder: str = None) -> None:
        super().__init__("select")
        self.attributes["name"] = name
        self.classes()
        with self:
            if placeholder:
                Element("option disabled selected", content=placeholder)
            for item in items:
                Element("option", content=item)
