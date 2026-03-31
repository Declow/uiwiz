from pathlib import Path
from typing import Literal

_type = Literal["info", "error", "success", "warning", "menu", "copy"]


def get_svg(svg: _type) -> str:
    if not svg:
        raise ValueError("Value cannot be None or an empty string")
    path = Path(__file__).parent / (svg + ".svg")
    with path.open() as f:
        return f.read()
