from uiwiz.element import Element
import markdown2


class Markdown(Element):
    def __init__(self, content="") -> None:
        super().__init__(content=content, render_html=False)

    def render_self(self, indent_level=0) -> str:
        return markdown2.markdown(self.content, extras=["fenced-code-blocks"])