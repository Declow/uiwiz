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
                                        Element(content=content + self.last_element("]", key == last_item))
                                    else:
                                        k.__content__ += " {"
                                        format_json(value, depth + 1)
                                        Element(content=content + self.last_element("}", value == last_item))
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
                        Element(tag="pre", content=f"{content}{self.format_key(item, obj[-1] == item)}").classes(
                            "text-primary"
                        )

        format_json(data)

    def format_key(self, value: str, last_element: bool) -> str:
        if not isinstance(value, numbers.Number):
            value = f'"{value}"'
        value = self.last_element(value, last_element)
        return str(value)

    def last_element(self, value: str, last_element) -> str:
        if not last_element:
            value = str(value) + ","
        return str(value)


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
        def format_data(
            data: Union[dict, list], depth: int = 0, last_item: bool = False, do_indent: bool = False, obj: bool = False
        ):
            indent = " " * depth

            if isinstance(data, list):
                last_item = data[-1]
                for item in data:
                    is_last = item == last_item
                    with Element().classes("flex flex-col flex-wrap"):
                        format_data(item, depth=depth + 2, last_item=is_last, do_indent=True)
                return
            if isinstance(data, dict):
                last_item = list(data.values())[-1]

                if not obj:
                    Element("pre", content=indent + "{")
                    indent += " " * 2
                for key, value in data.items():
                    is_last = last_item == value
                    key_content = indent + f'"{key}"' + ":"
                    if isinstance(value, list):
                        key_content += " ["
                        with Element(tag="pre", content=key_content).classes("flex flex-col flex-wrap"):
                            format_data(value, depth=depth + 2, last_item=is_last)
                        Element(tag="pre", content=indent + "]" + ("," if not is_last else ""))
                    elif isinstance(value, dict):
                        key_content += " {"
                        with Element(tag="pre", content=key_content).classes("flex flex-col flex-wrap"):
                            format_data(value, depth=depth + 2, last_item=is_last, obj=True)
                        Element(content=indent + "}" + ("," if not is_last else ""))
                    else:
                        with Element(tag="pre", content=key_content).classes("flex flex-row flex-wrap gap-2"):
                            format_data(value, depth=depth + 2, last_item=is_last)
                if not obj:
                    Element("pre", content=indent + "}")

                return

            if isinstance(data, str):
                with Element().classes("flex flex-row"):
                    out = f'"{data}"'
                    if do_indent:
                        out = indent + out
                    Element(tag="pre", content=out).classes("text-primary")
                    Element(tag="pre", content="," if not last_item else "")

            if isinstance(data, numbers.Number):
                with Element().classes("flex flex-row"):
                    out = str(data)
                    if do_indent:
                        out = indent + out
                    Element(tag="pre", content=out).classes("text-primary")
                    Element(tag="pre", content="," if not last_item else "")

        format_data(data)
