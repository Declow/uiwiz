import json
from pathlib import Path

from fastapi.responses import JSONResponse

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "echart.min.js"
JS_PATH = Path(__file__).parent / "echart.js"


class EChart(Element, extensions=[LIB_PATH, JS_PATH]):
    name: str = "data-wz-echart"

    def __init__(self, options: dict, height: str = "h-80") -> None:
        """EChart element

        See https://echarts.apache.org/examples/en/index.html for examples
        on how to use ECharts

        Example usage:
        .. code-block:: python

                from uiwiz import ui

                options = {
                    "title": {"text": "ECharts entry example"},
                    "tooltip": {},
                    "legend": {"data": ["Sales"]},
                    "xAxis": {"data": ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]},
                    "yAxis": {},
                    "series": [{"name": "Sales", "type": "bar", "data": [5, 20, 36, 10, 10, 20]}],
                }

                ui.echart(options)

        :param options: EChart options
        :param height: Height of the chart container
        """
        with Element() as container:
            container.classes(f"flex justify-center relative overflow-hidden items-center {height}")
            super().__init__()

        self.attributes[EChart.name] = EChart.name
        self.attributes[f"{EChart.name}-options"] = json.dumps(options)
        self.attributes["hx-ext"] = EChart.name
        self.classes("w-full h-full")

    def container_classes(self, input: str) -> "EChart":
        self.parent_element.classes(input)
        return self

    @staticmethod
    def response(data: dict, headers: dict[str, str] = {}) -> JSONResponse:
        _headers = {"HX-Trigger": json.dumps({"uiwizUpdateEChart": data})} | headers
        return JSONResponse(data, headers=_headers)
