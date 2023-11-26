from typing import Any, Callable, Optional, TypedDict


class Event(TypedDict):
    func: Callable
    inputs: list[Any]
    trigger: str
    endpoint: Optional[str]
    target: Optional[str]
    swap: Optional[str]
    include: Optional[str]
    vals: Optional[str]