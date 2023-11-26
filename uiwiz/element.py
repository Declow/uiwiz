import asyncio
from typing import Any, Callable, Optional, TypedDict
import random

from uiwiz.event import Event

class Frame:
    stacks: dict[int, "Frame"] = {}
    api = None

    def __init__(self) -> None:
        self.root_element: Optional[Element] = None
        self.current_element: Optional[Element] = None
        self.id = 0
        self.scripts: list[str] = []
        self.libraries: list[str] = []

    def remove_frame(self, element: "Element") -> None:
        if element is None:
            if self.root_element:
                self.root_element.stack = None
                self.remove_frame(self.root_element)
        else:
            element.stack = None
            for child in element.children:
                self.remove_frame(child)


    @classmethod
    def get_stack(cls) -> "Frame":
        _id = get_task_id()
        if _id not in cls.stacks:
            cls.stacks[_id] = Frame()
        return cls.stacks[_id]
    
    @classmethod
    def del_stack(cls):
        cls.get_stack().remove_frame(None)
        del cls.stacks[get_task_id()]
    

def get_task_id() -> int:
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0


class Element:
    def __init__(self, tag="div", indent_level=2, content="", render_html=True, libraries: Optional[str] = []) -> None:
        self.stack = Frame.get_stack()
        self.stack.libraries.extend(libraries)
        self.attributes: dict[str, str] = {}
        self.attributes["id"] = f"a-{self.stack.id}"
        self.stack.id += 1
        self.tag: str = tag

        self.event: Event = {}
        self.parent_element: Element = None
        self.children: list[Element] = []
        self.script: str = None
        self.render_html: bool = render_html
        self.target: str = None
        self.inline: bool = False

        self.content = content
        self.indent = indent_level

        
        if self.stack.root_element is None:
            self.stack.root_element = self
            self.stack.current_element = self
        else:
            self.stack.current_element.children.append(self)
            self.parent_element = self.stack.current_element

    def __enter__(self):
        self.stack.current_element = self
        return self
    
    def __exit__(self, *_):
        self.stack.current_element = self.parent_element
    
    @property
    def id(self):
        return self.attributes["id"]

    def classes(self, input: str):
        self.attributes["class"] = input
        return self

    def render(self, render_script: bool = True) -> str:
        output = self.render_self()
        if render_script and self.stack.scripts:
            output += "<script>"
            output += "(function () {"
            for script in self.stack.scripts:
                output += script
            output += "}());"
            output += "</script>"
        return output
    
    def render_self(self, indent_level = 0) -> str:
        output = ""
        self.before_render()
        if self.render_html:
            output = self.render_attributes(indent_level)
            if self.inline is False:
                output += "\n"
            output += self.content
            for child in self.children:
                output += child.render_self(indent_level + self.indent)
            if self.inline is False:
                output += " " * indent_level
            output += f"</{self.tag}>\n"
        if self.script:
            self.stack.scripts.append(self.script)
        return output

    def render_attributes(self, indent_level) -> str:
        output = " " * indent_level
        output += f'<{self.tag} '
        for key, value in self.attributes.items():
            output += f'{key}="{value}" '
        output = self.render_event(output)
        output += f'>'
        return output
        
    def before_render(self):
        pass

    def render_event(self, output) -> str:
        if self.event == {}:
            return output
        
        endpoint = self.event.get("endpoint")
        if endpoint is None:
            generator = random.Random(self.id)
            endpoint = "/" + "".join([str(generator.randrange(10)) for _ in range(20)])
        
        Frame.api(endpoint)(self.event["func"])
        target = self.event.get("target") if self.event.get("target") is not None else "this"
        swap = self.event.get("swap") if self.event.get("swap") is not None else "outerHTML"

        output += f'hx-post="{endpoint}" '
        if self.event.get("trigger"):
            output += f'hx-trigger="{self.event["trigger"]}" '

        if isinstance(target, Callable):
            _target = "next #" + str(target())
        else:
            _target = target

        output += f'hx-target="{_target}" '
        output += f'hx-swap="{swap}" '

        if vals:= self.event.get("vals"):
            output += f"hx-vals='{vals}' "
        if include:= self.event.get("include"):
            output += f'hx-include="{include}" '
        if hx_encoding:= self.event.get("hx-encoding"):
            output += f'hx-encoding="{hx_encoding}" '
        else:
            output += "hx-ext='json-enc' "

        return output
    
    def render_libs(self) -> str:
        output = ""
        for lib in self.stack.libraries:
            output += f'<script src="{lib}"></script>\n'
        return output
    
    def __str__(self) -> str:
        return self.render()
    
    def set_frame(self, frame: Frame):
        self.stack = frame
        for child in self.children:
            child.set_frame(frame)

    def set_frame_and_root(self) -> None:
        self.set_frame(Frame.get_stack())
        self.stack.root_element = self
