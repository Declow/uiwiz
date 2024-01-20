from typing import Callable, Optional, TypedDict


class Event(TypedDict):
    func: Callable
    trigger: str
    target: Optional[str]
    swap: Optional[str]
    include: Optional[str]
    vals: Optional[str]
