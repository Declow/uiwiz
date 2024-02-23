from uiwiz.elements.html import Html
import markdown2


class Code(Html):
    def __init__(self, code: str) -> None:
        super().__init__("div")
        color = "bg-neutral-content"
        _class = "mockup-window " + color

        self.classes(_class)

        self.content = markdown2.markdown(code, extras=["fenced-code-blocks"])
        self.content = self.content.replace("<pre>", f'<pre class="{color}"')
