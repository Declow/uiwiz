import numbers
from pathlib import Path
from typing import Iterable, Union

from uiwiz.element import Element


class Dict(Element):
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
        self._border_classes = "border border-base-content rounded-lg shadow-lg w-96 shadow-md w-full mb-5"

    def key_classes(self, classes):
        self.key_class = classes
        return self

    def value_classes(self, classes):
        self.value_class = classes
        return self

    def border_classes(self, classes: str):
        self._border_classes = classes
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
                    if do_indent:
                        Element(tag="pre", content=indent)
                    Element(content=f'"{data}"').classes(self.value_class)
                    Element(content="," if not is_last_item else "")

            if isinstance(data, numbers.Number):
                with Element().classes("flex flex-row"):
                    if do_indent:
                        Element(tag="pre", content=indent)
                    Element(content=str(data)).classes(self.value_class)
                    Element(tag="div", content="," if not is_last_item else "")

        with self.classes(self._border_classes):
            format_data(data, is_last_item=True)
