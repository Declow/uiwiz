from uiwiz.element import Element


class Dropdown(Element):
    root_class: str = "select "
    _classes: str = "select-bordered w-full max-w-xs"

    def __init__(self, name: str, items: list[str], placeholder: str = None) -> None:
        super().__init__("select")
        self.attributes["name"] = name
        self.classes()
        with self:
            if placeholder and placeholder not in items:
                Element("option disabled selected", content=placeholder)
            for v in items:
                e = Element("option", content=v)
                e.value = v
                if placeholder == v:
                    e.attributes["selected"] = "selected"
