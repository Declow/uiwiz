from typing import Optional

from uiwiz import ui
from uiwiz.asgi_request_middleware import get_request
from uiwiz.element import Element


class ThemeSelector(Element):
    def __init__(self, themes: Optional[list[str]] = None) -> None:
        super().__init__()
        self.render_html = False
        self.themes = [
            "light",
            "dark",
            "nord",
            "cupcake",
            "pastel",
            "bumblebee",
            "emerald",
            "corporate",
            "synthwave",
            "retro",
            "cyberpunk",
            "valentine",
            "halloween",
            "garden",
            "forest",
            "aqua",
            "lofi",
            "fantasy",
            "wireframe",
            "black",
            "luxury",
            "dracula",
            "cmyk",
            "autumn",
            "business",
            "acid",
            "lemonade",
            "night",
            "coffee",
            "winter",
            "dim",
            "sunset",
        ]
        if themes:
            self.themes = themes

        placeholder = "Theme"
        if theme := get_request().cookies.get("data-theme"):
            placeholder = theme

        self.theme_selector = ui.dropdown("theme-selector", self.themes, placeholder)
        self.theme_selector.classes("min-w-32")
        self.setup_listener()

    def setup_listener(self):
        self.script = f"""
function selectTheme(value) {{
    console.log(value);
    element = document.getElementById("html");
    element.setAttribute("data-theme", value);
    document.cookie = `data-theme=${{value}}; Path=/`; 
}}

document.getElementById("{self.theme_selector.id}").addEventListener('change', function() {{
    selectTheme(this.value);
}});
"""
