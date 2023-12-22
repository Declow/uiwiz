import asyncio
from typing import Callable, Optional
import random
from uiwiz.header_middelware import get_headers

from uiwiz.event import Event


class Frame:
    stacks: dict[int, "Frame"] = {}
    api = None

    def __init__(self) -> None:
        self.root_element: Optional[Element] = None
        self.current_element: Optional[Element] = None
        self.oob_elements: list[Element] = []
        self.used_hx_headers: bool = False
        self.id_count: int = 0  # used for element id
        self.element_id: str = self.get_id()  # Element id
        self.scripts: list[str] = []
        self.libraries: list[str] = []

    def get_id(self) -> str:
        headers = get_headers()
        out_id = ""
        if swap := headers.get("hx-swap"):
            target_id = headers.get("hx-target")
            if self.used_hx_headers is False:
                if swap == "outerHTML":
                    out_id = target_id
                else:
                    generator = random.Random(target_id)
                    out_id = f"a-{generator.randint(10000, 99999)}"
                self.used_hx_headers = True
                return out_id
            generator = random.Random(target_id)
            return f"a-{generator.randint(10000, 99999)}"

        return f"a-{self.id_count}"

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
    def __init__(
        self,
        tag="div",
        indent_level=2,
        content="",
        render_html=True,
        libraries: list[str] = [],
        oob: bool = False,
    ) -> None:
        self.stack = Frame.get_stack()
        self.stack.libraries.extend(libraries)
        self.attributes: dict[str, str] = {}
        self.attributes["id"] = self.stack.get_id()
        self.stack.id_count += 1
        self.tag: str = tag

        self.event: Event = {}
        self.parent_element: Element = None
        self.children: list[Element] = []
        self.script: str = None
        self.render_html: bool = render_html
        self.target: str = None
        self.inline: bool = False

        self.content: str = content
        self.indent: int = indent_level
        self.oob: bool = oob

        if self.oob:
            self.attributes["hx-swap-oob"] = "true"
            self.stack.oob_elements.append(self)

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

    @property
    def name(self):
        return self.attributes["name"]

    def get_classes(self) -> str:
        return self.attributes["class"]

    def classes(self, input: str = ""):
        self.attributes["class"] = getattr(self.__class__, "root_class", "") + input
        return self

    def render(self, render_script: bool = True) -> str:
        output = self.render_top_level(render_script)
        output += self.render_oob()
        return output

    def render_top_level(self, render_script: bool = True, render_oob: bool = False) -> str:
        output = self.render_self(render_oob=render_oob)
        if render_script and self.stack.scripts:
            output += "<script>"
            output += "(function () {"
            for script in self.stack.scripts:
                output += script
            output += "}());"
            output += "</script>"
        return output

    def render_self(self, indent_level: int = 0, render_oob: bool = False) -> str:
        if self.oob and render_oob is False:
            return ""
        output = ""
        self.before_render()
        if self.render_html:
            output = self.render_attributes(indent_level)
            if self.inline is False:
                output += "\n"
            output += self.content
            for child in self.children:
                if child.oob is False:
                    output += child.render_self(indent_level + self.indent)
            if self.inline is False:
                output += " " * indent_level
            output += f"</{self.tag}>\n"
        if self.script:
            self.stack.scripts.append(self.script)
        return output

    def render_attributes(self, indent_level: int) -> str:
        output = " " * indent_level
        output += f"<{self.tag} "
        for key, value in self.attributes.items():
            output += f'{key}="{value}" '
        output = self.render_event(output)
        output += ">"
        return output

    def before_render(self):
        pass

    def render_event(self, output: str) -> str:
        if self.event == {}:
            return output

        endpoint = self.event.get("endpoint")
        if endpoint is None:
            generator = random.Random(self.id)
            endpoint = "/" + "".join([str(generator.randrange(10)) for _ in range(20)])
            Frame.api.ui(endpoint)(self.event["func"])
        target = self.event.get("target") if self.event.get("target") is not None else "this"
        swap = self.event.get("swap") if self.event.get("swap") is not None else "outerHTML"

        output += f'hx-post="{endpoint}" '
        if self.event.get("trigger"):
            output += f'hx-trigger="{self.event["trigger"]}" '

        if isinstance(target, Callable):
            _target = "#" + str(target())
        else:
            _target = target

        output += f'hx-target="{_target}" '
        output += f'hx-swap="{swap}" '

        if vals := self.event.get("vals"):
            output += f"hx-vals='{vals}' "
        if include := self.event.get("include"):
            output += f'hx-include="{include}" '
        if hx_encoding := self.event.get("hx-encoding"):
            output += f'hx-encoding="{hx_encoding}" '
        else:
            output += "hx-ext='json-enc'"

        return output

    def render_libs(self) -> str:
        output = ""
        for lib in self.stack.libraries:
            output += f'<script src="{lib}"></script>\n'
        return output

    def render_oob(self) -> str:
        output = "\n"
        el: Element
        for el in self.stack.oob_elements:
            output += el.render_top_level(render_oob=True)
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
