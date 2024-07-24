import json
from typing import Optional, Union

from pydantic import BaseModel

from uiwiz.element import Element
from uiwiz.elements.checkbox import Checkbox
from uiwiz.elements.row import Row


class Json(Element):
    def __init__(self, data: Optional[Union[list, dict, str, BaseModel]]) -> None:
        if not data:
            raise ValueError("None type invalid for json element")
        self.generate(data)
        self.generate_v2(data)

    def generate(self, data: Union[list, dict]):
        def format_json(obj):
            if isinstance(obj, dict):
                with Element("ul").classes("collapsible"):
                    for key, value in obj.items():
                        with Element("li"):
                            with Element("span", f"{key}: ").classes("text-base-content"):
                                if isinstance(value, (dict, list)):
                                    with Element("span").classes("togglee"):
                                        Element("span", "▼").classes("toggle-icon")
                                        with Element().classes("nested"):
                                            format_json(value)
                                else:
                                    Element("span", json.dumps(value)).classes("text-primary")
            elif isinstance(obj, list):
                with Element("ul").classes("collapsible"):
                    for item in obj:
                        with Element("li"):
                            if isinstance(item, (dict, list)):
                                with Element("span", "▼").classes("togglee"):
                                    format_json(item)
                            else:
                                Element("span", json.dumps(item)).classes("text-primary")
            else:
                Element("span", json.dumps(obj)).classes("text-primary")

        format_json(data)

    def generate_v2(self, data):
        def format_json(obj):
            if isinstance(obj, dict):
                with Element().classes("bg-base-200 w-full"):
                    for key, value in obj.items():
                        with Element().classes("flex flex-row flex-wrap gap-2"):  # row
                            key_element = Element()
                            if isinstance(value, (dict, list)):
                                with key_element.classes("collapse collapse-arrow"):
                                    ch = Element("input")
                                    ch.attributes["type"] = "checkbox"
                                    ch.attributes["checked"] = "checked"
                                    Element(content=f"{key}:").classes("collapse-title min-h-0 p-0")
                                    with Element().classes("collapse-content"):
                                        format_json(value)
                            else:
                                key_element.content = f"{key}:"
                                Element("p", json.dumps(value)).classes("text-primary")

            #             with Element(content=f"{key}: ").classes("collapse-content"):
            #                 if isinstance(value, (dict, list)):
            #                     with Element().classes("collapse"):
            #                         Checkbox("??", True)
            #                         Element().classes("collapse-title text-xl font-medium")
            #                         format_json(value)
            #                 else:
            #                     Checkbox("??", True)
            #                     Element().classes("collapse-title text-xl font-medium")
            #                     with Element().classes("collapse-content"):
            #                         Element("p", json.dumps(value)).classes("text-primary")
            # # elif isinstance(obj, list):
            #     with Element().classes("collapse bg-base-200"):
            #         Checkbox("??", True)
            #         for item in obj:
            #             Element().classes("collapse-title text-xl font-medium")
            #             with Element(content=f"{item}: ").classes("text-base-content collapse-content"):
            #                 if isinstance(item, (dict, list)):
            #                     with Element("span", "▼").classes("togglee"):
            #                         format_json(item)
            #                 else:
            #                     Element("span", json.dumps(item)).classes("text-primary")
            # else:
            #     Element("span", json.dumps(obj)).classes("text-primary")

        format_json(data)
