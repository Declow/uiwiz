import asyncio
import html
import os
from pathlib import Path
from typing import Callable, Optional, Union
from uuid import uuid4

from uiwiz.asgi_request_middelware import get_request
from uiwiz.event import Event

# https://developer.mozilla.org/en-US/docs/Glossary/Void_element
VOID_ELEMENTS = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
]


class Frame:
    stacks: dict[int, "Frame"] = {}

    def __init__(self) -> None:
        self.root_element: Optional[Element] = None
        self.current_element: Optional[Element] = None
        self.oob_elements: list[Element] = []
        self.id_count: int = 0  # used for element id
        self.scripts: list[str] = []
        self.libraries: list[str] = []
        self.extensions: set[str] = set()
        self.app = get_request().app
        self.last_id = None

    def get_id(self) -> str:
        headers = get_request().headers
        swap = headers.get("hx-swap")

        if swap is None:
            return f"a-{self.id_count}"

        target_id = self.last_id if self.last_id else headers.get("hx-target")
        self.last_id = str(uuid4())

        if swap in ["outerHTML", "this"]:
            self.last_id = target_id

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

    def render_libs(self) -> str:
        if self.root_element:
            return self.root_element.render_js(self.libraries)
        return ""

    def render_ext(self) -> str:
        if self.root_element:
            return self.root_element.render_js(self.extensions)
        return ""

    def add_extension(self, path: Path):
        _, filename = os.path.split(path)
        prefix = "/_static/ext/"
        endpoint = prefix + filename
        self.extensions.add(endpoint)
        self.app.register_extension(path, prefix)

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
        content="",
        render_html=True,
        libraries: Optional[list[str]] = None,
        extension: Path = None,
        oob: bool = False,
    ) -> None:
        self.stack = Frame.get_stack()
        if libraries is None:
            libraries = []
        self.stack.libraries.extend(libraries)
        if extension:
            self.stack.add_extension(extension)
        self.attributes: dict[str, str] = {}
        self.attributes["id"] = self.stack.get_id()
        self.stack.id_count += 1
        self.tag: str = tag

        self.event: Event = {}
        self.parent_element: Element = None
        self.children: list[Element] = []
        self.script: Optional[str] = None
        self.render_html: bool = render_html
        self.target: Optional[str] = None

        self.__content__: str = ""
        self.content: str = content
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

    @property
    def value(self):
        return self.attributes["value"]

    @value.setter
    def value(self, value):
        self.attributes["value"] = value

    @property
    def content(self) -> str:
        return self.__content__

    @content.setter
    def content(self, content):
        self.__content__ = html.escape(str(content))

    @property
    def is_void_element(self) -> bool:
        if self.tag in VOID_ELEMENTS:
            return True
        return False

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
        lst = []
        lst.append(self.render_self(render_oob=render_oob))
        if render_script:
            for script in self.stack.scripts:
                lst.append(
                    """
                    <script>
                    (function() {
                    %s
                    }());
                    </script>
                    """
                    % script
                )
        return "".join(lst)

    def render_self(self, render_oob: bool = False) -> str:
        if self.oob and render_oob is False:
            return ""

        self.before_render()
        if self.script:
            self.stack.scripts.append(self.script)
        lst = []
        if self.render_html:
            self.add_event_to_attributes()

            lst.append("<%s %s>" % (self.tag, self.dict_to_attrs()))
            lst.append(self.content)
            lst.extend([child.render_self() if child.oob is False else "" for child in self.children])

            if not self.is_void_element:
                lst.append("</%s>" % self.tag)

        html = "".join(lst)
        return self.after_render(html)

    def render_oob(self) -> str:
        lst = []
        el: Element
        for el in self.stack.oob_elements:
            lst.append(el.render_top_level(render_oob=True))
        return "".join(lst)

    def before_render(self):
        pass

    def after_render(self, html: str):
        return html

    def add_event_to_attributes(self):
        if self.event == {}:
            return

        self.attributes["hx-target"] = self.get_target(self.event.get("target"))
        self.attributes["hx-swap"] = self.event.get("swap") if self.event.get("swap") is not None else "outerHTML"

        self.attributes["hx-post"] = self.get_endpoint()
        self.attributes["hx-trigger"] = self.event.get("trigger")

        if vals := self.event.get("vals"):
            self.attributes["hx-vals"] = vals
        if include := self.event.get("include"):
            self.attributes["hx-include"] = include
        if hx_encoding := self.event.get("hx-encoding"):
            self.attributes["hx-encoding"] = hx_encoding
        else:
            self.attributes["hx-ext"] = "json-enc"

    def get_endpoint(self) -> str:
        func = self.event["func"]
        endpoint: Optional[str] = self.stack.app.app_paths.get(func)
        if endpoint:
            if params := self.event.get("params"):
                return endpoint.format(**params)
            return endpoint

        endpoint = f"/_uiwiz/hash/{func.__hash__()}"
        if not self.stack.app.route_exists(endpoint):
            self.stack.app.ui(endpoint)(func)
        return endpoint

    def get_target(self, target: Union[Callable, str, "Element", None]) -> str:
        _target = "this"
        if target is None:
            return _target

        if isinstance(target, Callable):
            return "#%s" % str(target())

        if isinstance(target, Element):
            return "#%s" % target.id

        if target != "this" and "#" not in target:
            return "#" + target

        return target

    def render_js(self, lst_js: list[str]) -> str:
        lst = set()
        for lib in lst_js:
            lst.add('<script src="%s"></script>' % lib)
        return "".join(lst)

    def __str__(self) -> str:
        return self.render()

    def set_frame(self, frame: Frame):
        self.stack = frame
        for child in self.children:
            child.set_frame(frame)

    def set_frame_and_root(self) -> None:
        self.set_frame(Frame.get_stack())
        self.stack.root_element = self

    def dict_to_attrs(self):
        ATTR_NO_VALUE = object()
        return " ".join(
            (key if value is ATTR_NO_VALUE else '%s="%s"' % (key, value)) for key, value in self.attributes.items()
        )
