from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Literal, TypedDict, TypeVar, Union

if TYPE_CHECKING:
    from uiwiz.element import Element

TRIGGER_COMBINATIONS = Literal[
    "keydown[ctrlKey&&key=='Enter'], keydown[metaKey&&key=='Enter']",
    "keydown[key=='Enter']",
    "keydown[ctrlKey&&key=='Enter']",
    "keydown[metaKey&&key=='Enter']",
    "keydown[shiftKey&&key=='Enter']",
    "keydown[altKey&&key=='Enter']",
]

ON_EVENTS = TypeVar(
    Literal[
        "input",
        "change",
        "click",
        "focus",
        "blur",
        "submit",
        "reset",
        "keydown",
        "keyup",
        "keypress",
        "scroll",
        "copy",
        "cut",
        "paste",
    ]
    | TRIGGER_COMBINATIONS,
)

# HTMX Swap Events
# https://htmx.org/attributes/hx-swap/
SWAP_EVENTS = TypeVar(
    Literal[
        "innerHTML",
        "outerHTML",
        "textContent",
        "beforebegin",
        "afterbegin",
        "beforeend",
        "afterend",
        "delete",
        "none",
    ]
    | None,
)

TARGET_TYPE = Union[None, Callable[[], str], str, "Element"]
FUNC_TYPE = Callable | str


class Event(TypedDict):
    func: FUNC_TYPE
    trigger: ON_EVENTS
    target: TARGET_TYPE
    swap: SWAP_EVENTS
    include: str | None
    vals: str | None
    params: dict | None
