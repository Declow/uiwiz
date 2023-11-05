from uiwiz.element import Element

class Toast(Element):
    _classes: str = "alert alert-info"

    def __init__(self, message: str) -> None:
        # This toast thing is kind of a hack
        # Use the classes to render the html content
        # and javascript to place it correctly in the DOM.
        # Then some javascript runs on the client to
        # remove it from the DOM
        super().__init__(tag="div")
        self.classes(Toast._classes)
        e = Element("span", content=message)

        output = self.render(render_script_script=False).replace("\n", "")

        self.script = f"""
container = document.getElementById("toast");
$(container).prepend('{output}')""".replace("\n", " ")
        self.render_html = False
        e.render_html = False