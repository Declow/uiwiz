from uiwiz.element import Element


class Html(Element):
    def __init__(self, content) -> None:
        super().__init__()
        self.content = content
