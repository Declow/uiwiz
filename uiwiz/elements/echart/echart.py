from pathlib import Path
from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "echart.min.js"

class EChart(Element, extensions=[LIB_PATH]):
    def __init__(self) -> None:
        super().__init__()

        self.attributes["id"] = "echart"