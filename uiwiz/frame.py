import asyncio
import os
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, List, Optional, Union
from uuid import uuid4

from uiwiz.asgi_request_middleware import get_request
from uiwiz.version import __version__

if TYPE_CHECKING:
    from uiwiz.element import Element


def get_task_id() -> int:
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0


class Frame:
    stacks: dict[int, "Frame"] = {}

    def __init__(self) -> None:
        self.root: List["Element"] = []
        self.current_element: Optional["Element"] = None
        self.id_count: int = 0  # used for element id
        self.scripts: list[str] = []
        self.extensions: List[str] = []
        self.app = get_request().app
        self.last_id = None
        self.meta_description_content: str = ""

    def get_id(self) -> str:
        headers = get_request().headers
        swap = headers.get("hx-swap")

        if swap is None:
            return f"a-{self.id_count}"

        target_id = self.last_id if self.last_id else headers.get("hx-target")
        if swap.lower() in ["outerhtml", "this"] and self.last_id != target_id:
            self.last_id = target_id
        else:
            self.last_id = "a" + str(uuid4())

        return self.last_id

    def render(self) -> str:
        content = "".join([el.render() for el in self.root])
        self.del_stack()
        return content
    
    def add_extension(self, cls, extensions: Optional[Union[List[Path], Path]]) -> None:
        if extensions is None:
            return
        if not isinstance(extensions, Iterable):
            extensions = [extensions]

        for extension in extensions:
            _, filename = os.path.split(extension)
            prefix = f"/_static/extension/{__version__}/{cls.__name__}/"
            endpoint = prefix + filename
            if endpoint not in self.extensions:
                self.extensions.append(endpoint)

    @classmethod
    def get_stack(cls) -> "Frame":
        _id = get_task_id()
        if _id not in cls.stacks:
            cls.stacks[_id] = Frame()
        return cls.stacks[_id]

    @classmethod
    def del_stack(cls) -> None:
        del cls.stacks[get_task_id()]

    @classmethod
    def set_meta_description_content(cls, content: str) -> None:
        if isinstance(content, str) is False:
            raise Exception(f"Expected str got: {type(content)}")
        Frame.get_stack().meta_description_content = content
