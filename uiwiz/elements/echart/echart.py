from pathlib import Path

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "echart.min.js"
JS_PATH = Path(__file__).parent / "echart.js"


class EChart(Element, extensions=[LIB_PATH, JS_PATH]):
    def __init__(self, height: str = "h-80") -> None:
        with Element() as container:
            container.classes(f"flex justify-center relative overflow-hidden items-center {height}")
            super().__init__()
            self.attributes["id"] = "echart"
            self.classes("w-full h-full")
