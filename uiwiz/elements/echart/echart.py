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
            container.classes(f"flex justify-center relative overflow-hidden items-center {height}")
            super().__init__()
            self.attributes[EChart.name] = EChart.name
            self.attributes[f"{EChart.name}-options"] = json.dumps(options)
            self.classes("w-full h-full")

    @staticmethod
    def response(data: dict, headers: dict[str, str] = {}) -> JSONResponse:
        _headers = {"HX-Trigger": json.dumps({"uiwizUpdateEChart": data})} | headers
        return JSONResponse(data, headers=_headers)
