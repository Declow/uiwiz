import inspect
import json
from html import escape
from typing import Annotated, Callable, Optional

from fastapi import Depends, Request, Response

from uiwiz.element import Element
from uiwiz.frame import Frame
from uiwiz.version import __version__


class PageDefinition:
    html_ele: Element
    header_ele: Element
    body_ele: Element
    content_ele: Element
    title_ele: Element
    lang: str

    def __init__(self):
        """
        The PageDefinition class is designed to be subclassed, allowing
        developers to override the `header`, `body`, and `content` methods
        to customize the HTML structure and content as needed. The `footer`
        method can also be overridden to add custom footer content.

        This allows for a flexible and reusable page structure that can
        be easily extended for different pages in a web application or applied
        to all pages in a web application by setting the `page_definition_class`
        in the `UiwizApp` instance.


        ## Example:
        ```python
        from uiwiz import PageDefinition, Element

        class MyPage(PageDefinition):
            def header(self, header: Element) -> None:
                Element("link", href="/custom.css", rel="stylesheet")

            def body(self, body: Element) -> None:
                Element("div", content="Custom Body").classes("custom-body")

            def content(self, content: Element) -> Optional[Element]:
                return Element("h1", content="Custom Content").classes("custom-content")

            def footer(self, content: Element) -> None:
                Element("footer", content="Custom Footer").classes("custom-footer")
        ```

        """
        self._lang: str = "en"

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str) -> None:
        self._lang = value
        self.html_ele.attributes["lang"] = value

    @property
    def title(self) -> str:
        return self.title_ele.content

    @title.setter
    def title(self, value: str) -> None:
        self.title_ele.content = value

    async def render(
        self,
        user_method: Optional[Callable],
        request: Request,
        title: Optional[str] = None,
    ) -> Optional[Response]:
        frame = Frame.get_stack()

        theme = request.app.theme
        if cookie_theme := request.cookies.get("data-theme"):
            theme = escape(cookie_theme)

        class RenderDoctype:
            def render(self):
                return "<!DOCTYPE html>"

        frame.root.append(RenderDoctype())  # funky way to add doctype
        page_title = request.app.title if title is None else title
        with Element("html").classes("overflow-y-scroll") as html:
            self.html_ele = html

            html.attributes["id"] = "html"
            html.attributes["lang"] = self.lang
            if theme:
                html.attributes["data-theme"] = theme

            with Element("head") as header:
                self.header_ele = header

                Element("meta", name="viewport").attributes["content"] = "width=device-width, initial-scale=1"
                Element("meta", charset="utf-8")
                Element("meta", description=frame.meta_description_content)

                self.title_ele = Element("title", content=page_title)

                Element("link", href=f"/_static/{__version__}/libs/output.css", rel="stylesheet", type="text/css")
                Element("link", href=f"/_static/{__version__}/libs/daisyui.css", rel="stylesheet", type="text/css")
                Element(
                    "link", href=f"/_static/{__version__}/libs/daisyui-themes.css", rel="stylesheet", type="text/css"
                )
                Element("script", src=f"/_static/{__version__}/libs/tailwind.js")
                Element("link", href=f"/_static/{__version__}/app.css", rel="stylesheet", type="text/css")
                self.header(header)
            with Element("body") as body:
                self.body_ele = body

                body.attributes["hx-ext"] = "swap-header"
                self.body(body)
                with Element("div").classes("flex flex-col w-full min-h-screen") as content:
                    self.content_ele = content
                    user_content = self.content(content)
                    if user_content is not None:
                        if isinstance(user_content, Element):
                            self.content_ele = user_content
                        else:
                            raise TypeError(f"Expected Element, got {type(user_content).__name__} in content method")
                    with self.content_ele:
                        result = user_method()
                        if inspect.isawaitable(result):
                            result = await result
                        self.footer(content)

                toast = Element("div").classes("toast toast-top toast-end text-wrap z-50")
                toast.attributes["id"] = "toast"
                toast.attributes["hx-toast-delay"] = json.dumps({"delay": request.app.toast_delay})

            Element("script", src=f"/_static/{__version__}/libs/htmx1.9.9.min.js")
            Element("script", src=f"/_static/{__version__}/libs/htmx-json-enc.js")
            Element("script", src=f"/_static/{__version__}/default.js")

        return result

    def header(self, header: Element) -> None:
        pass

    def body(self, body: Element) -> None:
        pass

    def content(self, content: Element) -> Optional[Element]:
        pass

    def footer(self, content: Element) -> None:
        pass


Page = Annotated[PageDefinition, Depends()]
