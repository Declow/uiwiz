from pathlib import Path

import markdown2

from uiwiz.element import Element
from uiwiz.elements.html import Html

MARKDOWN = Path(__file__).parent / "markdown.css"
CODE_HIGHLIGHT = Path(__file__).parent / "codehighlight.css"


class Markdown(Element, extensions=[MARKDOWN, CODE_HIGHLIGHT]):
    def __init__(self, content="", extras=["fenced-code-blocks", "markdown-in-html"]) -> None:
        super().__init__()
        self.classes("markdown-body")
        self.extras = extras
        with self:
            _content = (
                markdown2.markdown(content, extras=self.extras)
                .replace("<ul>", '<ul class="list-disc">')
                .replace("<ol>", '<ol class="list-decimal">')
            )

            self.markdown = Html(content=_content)
