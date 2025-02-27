import html
import json
from pathlib import Path

from fastapi.responses import JSONResponse

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "echart.min.js"
JS_PATH = Path(__file__).parent / "echart.js"


class EChart(Element, extensions=[LIB_PATH, JS_PATH]):
    name: str = "data-wz-echart"

    def __init__(self, options: dict, height: str = "h-80") -> None:
        with Element() as container:
            self.parent_element = container
            container.classes(f"flex justify-center relative overflow-hidden items-center {height}")
            super().__init__()
            self.attributes[EChart.name] = EChart.name
            self.attributes[f"{EChart.name}-options"] = html.escape(json.dumps(options))
            self.attributes["hx-ext"] = EChart.name
            self.classes("w-full h-full")

    def container_classes(self, input: str) -> "EChart":
        self.parent_element.classes(input)
        return self

    @staticmethod
    def response(data: dict, headers: dict[str, str] = {}) -> JSONResponse:
        _headers = {"HX-Trigger": json.dumps({"uiwizUpdateEChart": data})} | headers
        return JSONResponse(data, headers=_headers)
