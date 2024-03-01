from uiwiz.elements.html import Html
import markdown2


class Markdown(Html):
    def __init__(self, content="") -> None:
        super().__init__(content=content)
        self.render_html = False
        self.classes("markdown-body")

    def render_self(self, *_) -> str:
        output = ""
        self.content = markdown2.markdown(self.content, extras=["fenced-code-blocks"])
        self.content = self.content.replace("<ul>", '<ul class="list-disc">')
        self.content = self.content.replace("<ol>", '<ol class="list-decimal">')
        self.render_html = True
        output = super().render_self()
        return output
