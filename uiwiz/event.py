from typing import Callable, Literal, Optional, TypedDict

ON_EVENTS = Literal[
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


class Event(TypedDict):
    func: Callable
    trigger: ON_EVENTS
    target: Optional[str]
    swap: Optional[str]
    include: Optional[str]
    vals: Optional[str]
    params: Optional[dict]
