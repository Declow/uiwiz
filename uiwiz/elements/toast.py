from uiwiz.element import Element
from uiwiz import ui
from uiwiz.svg.svg_handler import get_svg, _type

class Toast(Element):
    _classes: str = "alert w-64"

    def __init__(self, message: str, svg: _type = None) -> None:
        # This toast thing is kind of a hack
        # Use the classes to render the html content
        # and javascript to place it correctly in the DOM.
        # Then some javascript runs on the client to
        # remove it from the DOM
        super().__init__(tag="div")
        self.classes(Toast._classes)
        self.message = message
        self._svg = svg

    def svg(self, svg: _type) -> "Toast":
        self._svg = svg
        return self

    def render(self, render_script: bool = True) -> str:
        with self:
            if self._svg:
                ui.html(get_svg(self._svg))
            Element("span", content=self.message)  

        output = super().render(render_script=False)
        script = f"""
container = document.getElementById("toast");
$(container).prepend('{output}')""".replace("\n", " ")

        return f"<script>(function () {{ {script} }}());</script>"