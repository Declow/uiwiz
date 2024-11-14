from __future__ import annotations

import html
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from typing_extensions import Self

from uiwiz.element_types import ELEMENT_SIZE, ELEMENT_TYPES, VOID_ELEMENTS
from uiwiz.event import TARGET_TYPE, Event
from uiwiz.frame import Frame
from uiwiz.shared import register_resource


class Element:
    def __init__(
        self,
        tag: ELEMENT_TYPES = "div",
        content: str = "",
        render_html: bool = True,
        oob: bool = False,
    ) -> None:
        self.stack = Frame.get_stack()
        if hasattr(self.__class__, "extensions") and self.__class__.extensions:
            for extension in self.__class__.extensions:
                self.stack.add_extension(self.__class__, extension)
        self.attributes: dict[str, str] = {}
        self.attributes["id"] = self.stack.get_id()
        self.stack.id_count += 1
        self.tag: str = tag
        self._size: str = "md"

        self.event: Event = {}
        self.parent_element: Element = None
        self.children: list[Element] = []
        self.script: Optional[str] = None
        self.render_html: bool = render_html
        self.target: Optional[str] = None

        self.__content__: str = ""
        self.content: str = content
        self.oob: bool = oob

        self.classes()

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

    def __init_subclass__(cls, extensions: List[Path] = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.extensions = extensions
        if extensions:
            for extension in extensions:
                register_resource(f"{cls.__name__}/{extension.name}", extension)

    @property
    def id(self):
        return self.attributes.get("id")

    @property
    def name(self):
        return self.attributes.get("name")

    @property
    def value(self):
        return self.attributes.get("value")

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

    def classes(self, input: str = "") -> Self:
        """
        Set tailwind classes for the element.

        :param input: The tailwind classes to apply to the element.
        :return: The current instance of the element.
        """
        clazz = getattr(self.__class__, "root_class", "")
        if clazz == "":
            clazz = input
        elif input:
            clazz += f" {input}"
        if clazz:
            self.attributes["class"] = clazz
            self.size(self._size)
        return self

    def size(self, size: ELEMENT_SIZE) -> Self:
        """
        Set the size of the element.

        :param size: The size of the element.
        :return: The current instance of the element.
        """
        format = getattr(self.__class__, "root_size", "")
        if format:
            old_size = format.format(size=self._size)
            if old_size in self.attributes["class"]:
                self.attributes["class"] = self.attributes["class"].replace(
                    f"{old_size}", f"{format.format(size=size)}"
                )
            else:
                clazz = self.attributes["class"]
                if clazz == "":
                    self.attributes["class"] = format.format(size=size)
                else:
                    self.attributes["class"] = f"{self.attributes['class']} {format.format(size=size)}"
            self._size = size
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

            lst.append("<%s %s>" % (self.tag, self.__dict_to_attrs__()))
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

    def after_render(self, html: str) -> str:
        return html

    def add_event_to_attributes(self) -> None:
        if self.event == {}:
            return None

        self.attributes["hx-target"] = self.get_target(self.event.get("target"))
        self.attributes["hx-swap"] = self.event.get("swap") if self.event.get("swap") is not None else "outerHTML"

        self.attributes["hx-post"] = self.__get_endpoint__()
        self.attributes["hx-trigger"] = self.event.get("trigger")

        if vals := self.event.get("vals"):
            self.attributes["hx-vals"] = vals
        if include := self.event.get("include"):
            self.attributes["hx-include"] = include
        if hx_encoding := self.event.get("hx-encoding"):
            self.attributes["hx-encoding"] = hx_encoding
        else:
            self.attributes["hx-ext"] = "json-enc"

    def __get_endpoint__(self) -> str:
        func = self.event["func"]

        if isinstance(func, str):
            return func

        endpoint: Optional[str] = self.stack.app.app_paths.get(func)
        if endpoint:
            if params := self.event.get("params"):
                return endpoint.format(**params)
            return endpoint

        endpoint = f"/_uiwiz/hash/{func.__hash__()}"
        if not self.stack.app.route_exists(endpoint):
            self.stack.app.ui(endpoint)(func)
        return endpoint

    def get_target(self, target: TARGET_TYPE) -> str:
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

    def render_ext(self, lst_ext: list[str]) -> Tuple[str, str]:
        lst_js = []
        lst_css = []
        for lib in lst_ext:
            if lib.endswith("css"):
                css = '<link href="%s" rel="stylesheet" type="text/css" />' % lib
                if css not in lst_css:
                    lst_css.insert(0, css)
            elif lib.endswith("js"):
                js = '<script src="%s"></script>' % lib
                if js not in lst_js:
                    lst_js.append(js)
            else:
                raise Exception("lib type not supported, supported types css, js")
        return "".join(lst_js), "".join(lst_css)

    def __str__(self) -> str:
        return self.render()

    def set_frame(self, frame: Frame):
        self.stack = frame
        for child in self.children:
            child.set_frame(frame)

    def set_frame_and_root(self) -> None:
        self.set_frame(Frame.get_stack())
        self.stack.root_element = self

    def __dict_to_attrs__(self):
        ATTR_NO_VALUE = object()
        return " ".join(
            (key if value is ATTR_NO_VALUE else '%s="%s"' % (key, value)) for key, value in self.attributes.items()
        )
