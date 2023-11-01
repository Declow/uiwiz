import asyncio
from typing import Any, Callable, Optional, TypedDict

class Frame:
    stacks: dict[int, "Frame"] = {}
    api = None

    def __init__(self) -> None:
        self.root_element: Element = None
        self.current_element: Element = None
        self.id = 0
        self.scripts: list[str] = []

    @classmethod
    def get_stack(cls) -> "Frame":
        _id = get_task_id()
        print(_id)
        if _id not in cls.stacks:
            cls.stacks[_id] = Frame()
        return cls.stacks[_id]
    
    @classmethod
    def del_stack(cls):
        del cls.stacks[get_task_id()]
    

def get_task_id() -> int:
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0

class Event(TypedDict):
    func: Callable
    inputs: list[Any]
    _type: str
    endpoint: Optional[str]
    target: Optional[str]
    swap: Optional[str]


class Element:
    def __init__(self, tag="div", indent_level=2, content="", render_html=True) -> None:
        self.stack = Frame.get_stack()
        self.id: str = f"a-{self.stack.id}"
        self.stack.id += 1
        self.tag: str = tag
        self._classes: str = ""
        self.placeholder: str = None
        self.name: str = None
        self.auto_complete: bool = True
        self.events: list[Event] = []
        self.style = []
        self.parent_element: Element = None
        self.children: list[Element] = []
        self.script: str = None
        self.render_html: bool = render_html
        self.on_change: Callable = None
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

    def classes(self, input: str):
        self._classes = input
        return self

    def render(self, indent_level = 0, render_script_script: bool = True) -> str:
        output = self.render_self()
        if render_script_script:
            output += "<script>"
            for script in self.stack.scripts:
                output += script
            output += "</script>"
        return output
    
    def render_self(self, indent_level = 0) -> str:
        output = ""
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
        output += f'id="{self.id}" '
        if self._classes:
            output += f'class="{self._classes}" '

        if self.placeholder:
            output += f'placeholder="{self.placeholder}" '
        if self.name:
            output += f'name="{self.name}" '
        if self.tag == "form":
            output += f'target="{self.target}" '
        if not self.auto_complete:
            output += f'autocomplete="off"'
        output = self.render_events(output)
        output += f'>'
        return output

    def render_events(self, output) -> str:
        for event in self.events:
            endpoint = event.get("endpoint")
            if endpoint is None:
                endpoint = "/" + str(hash(frozenset(event.items())))
            
            Frame.api(endpoint)(event["func"])
            target = event.get("target") if event.get("target") is not None else "this"
            swap = event.get("swap") if event.get("swap") is not None else "outerHTML"

            output += f'hx-post="{endpoint}" '
            output += f'hx-trigger="{event["_type"]}" '

            if isinstance(target, Callable):
                _target = "next #" + str(target())
            else:
                _target = target

            output += f'hx-target="{_target}" '
            output += f'hx-swap="{swap}" '
            output += "hx-ext='json-enc' "

        return output
    
    def __str__(self) -> str:
        return self.render()
