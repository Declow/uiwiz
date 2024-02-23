from typing import Literal
from anyio import Path

_type = Literal[
    "info",
    "error",
    "success",
    "warning",
    "menu",
    None,
]


def get_svg(svg: Literal["info", "error", "success", "warning", "menu", "uiwiz"]) -> str:
    path = Path(__file__).parent / (svg + ".svg")
    with open(path, "r") as f:
        return f.read()
