import json
from typing import Optional, Union

from pydantic import BaseModel

from uiwiz.element import Element


class Json(Element):
    def __init__(self, data: Optional[Union[list, dict, str, BaseModel]]) -> None:
        if not data:
            raise ValueError("None type invalid for json element")
        self.generate(data)

    def generate(self, data: Union[list, dict]):
        def format_json(obj):
            if isinstance(obj, dict):
                with Element("ul").classes("collapsible"):
                    for key, value in obj.items():
                        with Element("li"):
                            with Element("span", key).classes("key"):
                                if isinstance(value, (dict, list)):
                                    with Element("span").classes("togglee"):
                                        Element("span", "▼").classes("toggle-icon")
                                        with Element().classes("nested"):
                                            format_json(value)
                                else:
                                    Element("span", json.dumps(value)).classes("value")
            elif isinstance(obj, list):
                with Element("ul").classes("collapsible"):
                    for item in obj:
                        with Element("li"):
                            if isinstance(item, (dict, list)):
                                with Element("span", "▼").classes("togglee"):
                                    format_json(item)
                            else:
                                Element("span", json.dumps(item)).classes("value")
            else:
                Element("span", json.dumps(obj)).classes("value")

        format_json(data)
