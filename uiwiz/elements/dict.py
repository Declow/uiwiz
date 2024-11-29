import numbers
from typing import Iterable, Union

from uiwiz.element import Element
from uiwiz.elements.html import Html


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
                with Element().classes("border border-base-content rounded-lg shadow-lg w-96 shadow-md w-full mb-5"):
                    last_item = list(obj.values())[-1]
                    for key, value in obj.items():
                        with Element().classes("flex flex-row flex-wrap gap-2"):  # row
                            key_element = Element()
                            if isinstance(value, (dict, list)):
                                with key_element.classes("collapse collapse-arrow pl-1"):
                                    ch = Element("input")
                                    ch.attributes["type"] = "checkbox"
                                    ch.attributes["checked"] = "checked"
                                    Element(content=f"{key}:").classes("collapse-title text-sm min-h-8 p-0")
                                    with Element().classes("collapse-content"):
                                        format_json(value)
                            else:
                                key_element.content = f'"{key}":'
                                key_element.classes("pl-2")
                                if not isinstance(value, numbers.Number):
                                    value = f'"{value}"'
                                if not (last_item == value):
                                    value = str(value) + ","
                                Element("p", value).classes("text-primary pl-1")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        format_json(item)
                    else:
                        Element(content=item)
            else:
                Element(content=obj).classes("text-primary")

        format_json(data)


class DictV2(Element):
    def __init__(self, data: Union[Iterable[dict], dict]) -> None:
        if not data:
            raise ValueError("Data cannot be None or empty")
        if not isinstance(data, (Iterable, dict)):
            raise ValueError("Data not of type list or dict")
        super().__init__()
        with self.classes("border border-base-content rounded-lg shadow-lg w-96 shadow-md w-full mb-5"):
            self.generate(data)

    def generate(self, data):
        def format_json(obj, depth: int = 0):
            content = " " * depth
            if isinstance(obj, dict):
                with Element():
                    last_item = list(obj.values())[-1]
                    for key, value in obj.items():
                        with Element().classes("flex flex-row flex-wrap"):  # row
                            key_element = Element()
                            if isinstance(value, (dict, list)):
                                with key_element:
                                    with Element(tag="pre", content=f'{content}"{key}":').classes("pl-2") as k:
                                        if isinstance(value, list):
                                            k.__content__ += " ["
                                            format_json(value, depth + 1)
                                            Element(content=content + "]")
                                        else:
                                            k.__content__ += " {"
                                            format_json(value, depth + 1)
                                            Element(content=content + "}")
                            else:
                                key_element.content = f'{content}"{key}":'
                                key_element.classes("pl-2")
                                value = self.format_key(value, last_item == value)
                                Element("pre", value).classes("text-primary pl-1")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        format_json(item, depth + 2)
                    else:
                        content = " " * (depth + 2)
                        Element(tag="pre", content=f'{content}{self.format_key(item, obj[-1] == item)}').classes("text-primary")

        format_json(data)

    def format_key(self, value: str, last_item: bool) -> str:
        if not isinstance(value, numbers.Number):
            value = f'"{value}"'
        if not last_item:
            value = str(value) + ","
        return str(value)
