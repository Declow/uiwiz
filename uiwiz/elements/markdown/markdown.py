from pathlib import Path

import markdown2

from uiwiz.elements.html import Html

MARKDOWN = Path(__file__).parent / "markdown.css"
CODE_HIGHLIGHT = Path(__file__).parent / "codehighlight.css"


class Markdown(Html, extensions=[MARKDOWN, CODE_HIGHLIGHT]):
    def __init__(self, content="", extras=["fenced-code-blocks", "markdown-in-html"]) -> None:
        super().__init__(content=content)
        self.render_html = False
        self.classes("markdown-body")
        self.extras = extras

    def render_self(self, *args, **kwargs) -> str:
        output = ""
        self.content = markdown2.markdown(self.content, extras=self.extras)
        self.content = self.content.replace("<ul>", '<ul class="list-disc">')
        self.content = self.content.replace("<ol>", '<ol class="list-decimal">')
        self.render_html = True
        output = super().render_self(*args, **kwargs)
        return output
