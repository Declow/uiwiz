from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple, Union
from uuid import uuid4

from uiwiz.asgi_request_middelware import get_request
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
        self.root_element: Optional[Element] = None
        self.current_element: Optional[Element] = None
        self.oob_elements: list[Element] = []
        self.id_count: int = 0  # used for element id
        self.scripts: list[str] = []
        self.extensions: List[str] = []
        self.app = get_request().app
        self.last_id = None
        self.title: Optional[str] = None
        self.meta_description_content: str = ""
        self.head_ext: str = ""

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

    def remove_frame(self, element: "Element") -> None:
        if element is None:
            if self.root_element:
                self.root_element.stack = None
                self.remove_frame(self.root_element)
        else:
            element.stack = None
            for child in element.children:
                self.remove_frame(child)

    def render(self) -> str:
        if self.root_element:
            return self.root_element.render()
        if self.oob_elements:
            output = ""
            el: Element
            for el in self.oob_elements:
                output += el.render_top_level()
            return output
        return ""

    def render_ext(self) -> Tuple[str, str]:
        if self.root_element:
            return self.root_element.render_ext(self.extensions)
        return "", ""

    def add_extension(self, cls, extensions: Optional[Union[list[Path], Path]]) -> None:
        if extensions is None:
            return
        if not isinstance(extensions, list):
            extensions = [extensions]

        for extension in extensions:
            _, filename = os.path.split(extension)
            prefix = f"/_static/extension/{__version__}/{cls.__name__}/"
            endpoint = prefix + filename
            if extension not in self.extensions:
                self.extensions.append(endpoint)

    @classmethod
    def get_stack(cls) -> "Frame":
        _id = get_task_id()
        if _id not in cls.stacks:
            cls.stacks[_id] = Frame()
        return cls.stacks[_id]

    @classmethod
    def del_stack(cls) -> None:
        cls.get_stack().remove_frame(None)
        del cls.stacks[get_task_id()]

    @classmethod
    def set_title(cls, title: str) -> None:
        if isinstance(title, str) is False:
            raise Exception(f"Expected str got: {type(title)}")
        Frame.get_stack().title = title

    @classmethod
    def set_meta_description_content(cls, content: str) -> None:
        if isinstance(content, str) is False:
            raise Exception(f"Expected str got: {type(content)}")
        Frame.get_stack().meta_description_content = content
