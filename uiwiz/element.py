import asyncio
from typing import Any, Callable, Optional, TypedDict

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

class Event(TypedDict):
    func: Callable
    inputs: list[Any]
    trigger: str
    endpoint: Optional[str]
    target: Optional[str]
    swap: Optional[str]
    include: Optional[str]
    vals: Optional[str]


class Element:
    def __init__(self, tag="div", indent_level=2, content="", render_html=True, libraries: Optional[str] = []) -> None:
        self.stack = Frame.get_stack()
        self.stack.libraries.extend(libraries)
        self.attributes: dict[str, str] = {}
        self.attributes["id"] = f"a-{self.stack.id}"
        self.stack.id += 1
        self.tag: str = tag

        self.auto_complete: bool = True
        self.events: list[Event] = []
        self.parent_element: Element = None
        self.children: list[Element] = []
        self.script: str = None
        self.render_html: bool = render_html
        self.target: str = "dummyframe" # See default template for hack

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
        if render_script:
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
            if self.children:
                output += "\n"
                for child in self.children:
                    output += child.render_self(indent_level + self.indent)
                output += " " * indent_level + f"</{self.tag}>\n"
            else:
                output += self.content
                output += f"</{self.tag}>\n"
        if self.script:
            self.stack.scripts.append(self.script)
        return output

    def render_attributes(self, indent_level) -> str:
        output = " " * indent_level
        output += f'<{self.tag} '
        for key, value in self.attributes.items():
            output += f'{key}="{value}" '
        if not self.auto_complete:
            output += f'autocomplete="off"'
        output = self.render_events(output)
        output += f'>'
        return output
        
    def before_render(self):
        pass

    def render_events(self, output) -> str:
        for event in self.events:
            endpoint = event.get("endpoint")
            if endpoint is None:
                endpoint = "/" + str(hash(frozenset(event.items())))
            
            Frame.api(endpoint)(event["func"])
            target = event.get("target") if event.get("target") is not None else "this"
            swap = event.get("swap") if event.get("swap") is not None else "outerHTML"
            vals = event.get("vals")
            include = event.get("include")
            hx_encoding = event.get("hx-encoding")

            output += f'hx-post="{endpoint}" '
            if event.get("trigger"):
                output += f'hx-trigger="{event["trigger"]}" '

            if isinstance(target, Callable):
                _target = "next #" + str(target())
            else:
                _target = target

            output += f'hx-target="{_target}" '
            output += f'hx-swap="{swap}" '

            if vals:
                output += f"hx-vals='{vals}' "
            if include:
                output += f'hx-include="{include}" '
            if hx_encoding:
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
