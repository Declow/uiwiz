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
        with self:
            if svg:
                ui.html(get_svg(svg))
            Element("span", content=message)

        output = self.render(render_script=False)

        self.script = f"""
container = document.getElementById("toast");
$(container).prepend('{output}')""".replace("\n", " ")
        self.render_html = False