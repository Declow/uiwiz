from typing import TYPE_CHECKING, Callable, Literal, Optional, TypedDict, Union

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

ON_EVENTS = Union[
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
    ],
    TRIGGER_COMBINATIONS,
]

# HTMX Swap Events
# https://htmx.org/attributes/hx-swap/
SWAP_EVENTS = Optional[
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
]

TARGET_TYPE = Optional[Union[Callable[[], str], str, "Element", None]]
FUNC_TYPE = Union[Callable, str]


class Event(TypedDict):
    func: FUNC_TYPE
    trigger: ON_EVENTS
    target: TARGET_TYPE
    swap: SWAP_EVENTS
    include: Optional[str]
    vals: Optional[str]
    params: Optional[dict]
