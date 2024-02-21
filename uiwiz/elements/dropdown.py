from uiwiz.element import Element
from uiwiz.request_middelware import get_request


class Dropdown(Element):
    root_class: str = "select "
    _classes: str = "select-bordered w-full max-w-xs"

    def __init__(self, name: str, items: list[str], placeholder: str = None) -> None:
        super().__init__("select")
        self.attributes["name"] = name
        self.classes()
        if theme := get_request().cookies.get("data-theme"):
            placeholder = theme
        with self:
            if placeholder and placeholder not in items:
                Element("option disabled selected", content=placeholder)
            for item in items:
                e = Element("option", content=item)
                e.value = item
                if placeholder == item:
                    e.attributes["selected"] = "selected"
