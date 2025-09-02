import typing
from typing import Literal, Optional

from uiwiz import ui
from uiwiz.asgi_request_middleware import get_request
from uiwiz.element import Element

THEMES = Literal[
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


class ThemeSelector(Element):
    def __init__(self, themes: Optional[THEMES] = None) -> None:
        """Theme Selector
        A dropdown to select a theme for the application.
        The selected theme will be stored in a cookie named "data-theme".

        Example:
        .. code-block:: python

            from uiwiz import ui

            ui.themeSelector(["light", "dark", "nord", "cupcake", "pastel", "bumblebee"])
        
        """
        super().__init__()
        self.render_html = False
        self.themes = list(typing.get_args(THEMES))
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
