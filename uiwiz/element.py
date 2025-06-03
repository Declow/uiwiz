import html
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

from typing_extensions import Self

from uiwiz.element_types import ELEMENT_SIZE, ELEMENT_TYPES, VOID_ELEMENTS
from uiwiz.event import FUNC_TYPE, TARGET_TYPE, Event
from uiwiz.frame import Frame
from uiwiz.shared import fetch_route, register_resource, route_exists


class _Attributes(dict):
    def __setitem__(self, key: Any, value: Any, escape: bool = True) -> None:
        if escape:
            if isinstance(value, str):
                value = html.escape(value)
            elif isinstance(value, bool):
                value = str(value).lower()
        super().__setitem__(key, value)


class Element:
    def __init__(
        self,
        tag: ELEMENT_TYPES = "div",
        content: str = "",
        render_html: bool = True,
        oob: bool = False,
        **kwargs: Optional[dict[str, str]],
    ) -> None:
        """Element

        Represents an HTML element. This class is used to create HTML elements.

        It is possible to create a custom element by subclassing this class.

        Content of any element will be escaped by default. If you want to render
        the content as HTML, you can use the ui.html(content="&lt;div&gt;html content&lt;/div&gt;") element.

        The rendering of the element is done by calling the render method.
        If some work needs to be done before or after rendering, the before_render
        and after_render methods can be overridden.

        The element attributes can be accessed and modified through the attributes property.
        The content of an attribute can either be a string or a callable that returns a string.

        Example:
        .. code-block:: python
            from uiwiz import ui

            ui.element("h1", "Hello World")


        :param tag: The tag of the element type
        :type tag: str
        :param content: The content of the element
        :type content: str, optional
        :param render_html: If the element should be rendered
        :type render_html: bool, optional
        :param oob: If the element should be out of band swap
        :type oob: bool, optional
        :param kwargs: The attributes of the element
        :type kwargs: dict[str, str], optional
        """
        self.stack = Frame.get_stack()
        if hasattr(self.__class__, "extensions") and self.__class__.extensions:
            for extension in self.__class__.extensions:
                self.stack.add_extension(self.__class__, extension)
        self.attributes: dict[str, Union[str, Callable[[], str]]] = _Attributes()
        if kwargs:
            self.attributes.update(kwargs)
        self.attributes["id"] = self.stack.get_id()
        self.stack.id_count += 1
        self.tag: str = tag
        self._size: str = "md"

        self.event: Event = {}
        self.parent_element: Optional[Element] = self.stack.current_element
        self.external_tree_element: Optional[Element] = None
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
            self.stack.root.append(self)
            self.stack.current_element = self
        elif self.parent_element is None:
            self.stack.root.append(self)
        else:
            self.stack.current_element.children.append(self)
            self.parent_element = self.stack.current_element

    def __enter__(self):
        if self.stack.current_element and self.parent_element and self.stack.current_element != self.parent_element:
            self.external_tree_element = self.stack.current_element
        self.stack.current_element = self

        return self

    def __exit__(self, *_):
        if self.external_tree_element:
            self.stack.current_element = self.external_tree_element
            self.external_tree_element = None
        else:
            self.stack.current_element = self.parent_element

    def __init_subclass__(cls, extensions: List[Path] = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.extensions = extensions
        if extensions:
            for extension in extensions:
                register_resource(f"{cls.__name__}/{extension.name}", extension)

    @property
    def id(self):
        """Get the id of the element."""
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
        """Get html classes of the element.

        :return: The classes of the element.
        :type: str
        """
        return self.attributes["class"]

    def classes(self, input: str = "") -> Self:
        """
        Set tailwind classes for the element.

        :param input: The tailwind classes to apply to the element.
        :return: The current instance of the element.
        """

        clazz = (
            getattr(self, "__root_class__", "")
            if hasattr(self, "__root_class__")
            else getattr(self.__class__, "root_class", "")
        )
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
        """
        Render the element as HTML.
        :param render_script: If any element has a javascript script, it will be rendered as well.
        :type render_script: bool
        """
        lst = []
        lst.append(self.__render_self__())
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

    def __render_self__(self) -> str:
        self.before_render()
        if self.script:
            self.stack.scripts.append(self.script)
        lst = []
        if self.render_html:
            self.__add_event_to_attributes__()

            lst.append("<%s %s>" % (self.tag, self.__dict_to_attrs__()))
            lst.append(self.content)
            lst.extend([child.__render_self__() if child.oob is False else "" for child in self.children])

            if not self.is_void_element:
                lst.append("</%s>" % self.tag)

        html = "".join(lst)
        return self.after_render(html)

    def before_render(self):
        """This method is called before the element is rendered."""
        pass

    def after_render(self, html: str) -> str:
        """This method is called after the element is rendered.

        :param html: The rendered HTML of the element."""
        return html

    def __add_event_to_attributes__(self) -> None:
        if self.event == {}:
            return None

        self.attributes["hx-target"] = self.__get_target__(self.event.get("target"))
        self.attributes["hx-swap"] = self.event.get("swap") if self.event.get("swap") is not None else "outerHTML"

        self.attributes["hx-post"] = self.__get_endpoint__(self.event["func"])
        self.attributes["hx-trigger"] = self.event.get("trigger")

        if vals := self.event.get("vals"):
            self.attributes["hx-vals"] = vals
        if include := self.event.get("include"):
            self.attributes["hx-include"] = include
        if hx_encoding := self.event.get("hx-encoding"):
            self.attributes["hx-encoding"] = hx_encoding
        else:
            self.attributes["hx-ext"] = "json-enc"

    def __get_endpoint__(self, func: FUNC_TYPE) -> str:
        if isinstance(func, str):
            return func

        endpoint: Optional[str] = fetch_route(func)
        if endpoint:
            if params := self.event.get("params"):
                return endpoint.format(**params)
            return endpoint

        endpoint = f"/_uiwiz/hash/{func.__hash__()}"
        if not route_exists(endpoint):
            self.stack.app.ui(endpoint)(func)
        return endpoint

    def __get_target__(self, target: TARGET_TYPE) -> str:
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

    def __str__(self) -> str:
        return self.render()

    def __set_frame__(self, frame: Frame):
        self.stack = frame
        for child in self.children:
            child.__set_frame__(frame)

    def _set_frame_and_root(self) -> None:
        self.__set_frame__(Frame.get_stack())
        self.stack.root.append(self)

    def __dict_to_attrs__(self):
        ATTR_NO_VALUE = object()
        return " ".join(
            (
                key
                if value is ATTR_NO_VALUE
                else ('%s="%s"' % (key, value()) if callable(value) else '%s="%s"' % (key, value))
            )
            for key, value in self.attributes.items()
        )
