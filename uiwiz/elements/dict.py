from typing import Iterable, Union

from uiwiz.element import Element


class Dict(Element):
    def __init__(self, data: Union[Iterable[dict], dict]) -> None:
        if not data:
            raise ValueError("Data cannot be None or empty")
        if not isinstance(data, (Iterable, dict)):
            raise ValueError("Data not of type list or dict")
        super().__init__()
        self.generate(data)

    def generate(self, data):
        def format_json(obj):
            if isinstance(obj, dict):
                with Element().classes("card w-96 bg-base-100 shadow-md w-full mb-5"):
                    for key, value in obj.items():
                        with Element().classes("flex flex-row flex-wrap gap-2"):  # row
                            key_element = Element()
                            if isinstance(value, (dict, list)):
                                with key_element.classes("collapse collapse-arrow pl-2"):
                                    ch = Element("input")
                                    ch.attributes["type"] = "checkbox"
                                    ch.attributes["checked"] = "checked"
                                    Element(content=f"{key}:").classes("collapse-title text-sm min-h-8 p-0")
                                    with Element().classes("collapse-content"):
                                        format_json(value)
                            else:
                                key_element.content = f"{key}:"
                                key_element.classes("pl-2")
                                Element("p", value).classes("text-primary pl-2")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        format_json(item)
                    else:
                        Element(content=item)
            else:
                Element(content=obj).classes("text-primary")

        format_json(data)
