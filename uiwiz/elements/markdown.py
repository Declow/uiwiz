from uiwiz.element import Element
import markdown2


class Markdown(Element):
    def __init__(self, content="") -> None:
        super().__init__(content=content, render_html=False)

    def render_self(self, *_) -> str:
        output = ""
        self.classes("markdown-body")
        self.content = markdown2.markdown(self.content, extras=["fenced-code-blocks"])
        self.content = self.content.replace("<ul>", '<ul class="list-disc">')
        self.content = self.content.replace("<ol>", '<ol class="list-decimal">')
        self.render_html = True
        output = super().render_self()
        return output
