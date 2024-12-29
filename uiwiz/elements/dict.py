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
        self.data = data
        self.did_render = False
        self.key_class = ""
        self.value_class = "text-primary"

    def key_classes(self, classes):
        self.key_class = classes
        return self

    def value_classes(self, classes):
        self.value_class = classes
        return self

    def before_render(self):
        super().before_render()
        if not self.did_render:
            self.did_render = True
            self.generate(self.data)

    def generate(self, data):
        def format_data(
            data: Union[dict, list],
            depth: int = 0,
            is_last_item: bool = False,
            do_indent: bool = False,
            obj: bool = False,
        ):
            indent = " " * depth

            if isinstance(data, list):
                last_item = data[-1]
                Element("pre", content=indent + "[")
                for item in data:
                    is_last = item == last_item
                    with Element().classes("flex flex-col flex-wrap"):
                        format_data(item, depth=depth + 2, is_last_item=is_last, do_indent=True)
                Element("pre", content=indent + "]")
                return
            if isinstance(data, dict):
                last_item = list(data.values())[-1]
                is_last = data == last_item

                if not obj:
                    Element("pre", content=indent + "{")
                    format_data(data, depth=depth + 2, is_last_item=is_last, obj=True)
                else:
                    for key, value in data.items():
                        is_last = last_item == value
                        key_content = indent + f'"{key}"' + ":"
                        if isinstance(value, list):
                            key_content += " ["
                            with Element(tag="pre", content=key_content).classes("flex flex-col flex-wrap"):
                                for _item in value:
                                    format_data(_item, depth=depth + 2, is_last_item=_item == value[-1], do_indent=True)
                            Element(tag="pre", content=indent + "]" + ("," if not is_last else ""))
                        elif isinstance(value, dict):
                            key_content += " {"
                            with Element(tag="pre", content=key_content).classes("flex flex-col flex-wrap"):
                                format_data(value, depth=depth + 2, is_last_item=is_last, obj=True)
                            Element(tag="pre", content=indent + "}" + ("," if not is_last else ""))
                        else:
                            with Element(tag="pre", content=key_content).classes("flex flex-row flex-wrap gap-2"):
                                format_data(value, depth=depth + 2, is_last_item=is_last)
                if not obj:
                    Element("pre", content=indent + "}" + ("," if not is_last_item else ""))

                return

            if isinstance(data, str):
                with Element().classes("flex flex-row"):
                    out = f'"{data}"'
                    if do_indent:
                        out = indent + out
                    Element(tag="pre", content=out).classes(self.value_class)
                    Element(tag="pre", content="," if not is_last_item else "")

            if isinstance(data, numbers.Number):
                with Element().classes("flex flex-row"):
                    out = str(data)
                    if do_indent:
                        out = indent + out
                    Element(tag="pre", content=out).classes(self.value_class)
                    Element(tag="pre", content="," if not is_last_item else "")

        with self.classes("border border-base-content rounded-lg shadow-lg w-96 shadow-md w-full mb-5"):
            format_data(data, is_last_item=True)
