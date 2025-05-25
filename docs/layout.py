from uiwiz import PageDefinition, ui
from uiwiz.svg.svg_handler import get_svg


class Layout(PageDefinition):
    def __init__(self) -> None:
        """Layout

        A layout element that provides a consistent structure for the application.
        """
        super().__init__()
        self.drawer = None
        self._nav = None
        self.hide_on = "md"
        self.page_route_container = None

    def content(self, element: ui.element):
        self.page_route_container = element
        self.drawer = ui.drawer()
        with self.drawer:
            with self.drawer.drawer_content() as content:
                self.nav(self.drawer)

        self.content_ele = content

    def footer(self, _: ui.element):
        with self.page_route_container:
            with ui.footer():
                with ui.element().classes("flex flex-col items-center justify-center"):
                    with ui.element("div").classes("flex flex-col items-center justify-center"):
                        ui.label("Made with ❤️ by Uiwiz").classes("text-sm")
                        ui.link("GitHub", "https://github.com/declow/uiwizard")

    def nav(self, drawer):
        with ui.element().classes(
            "sticky top-0 flex h-16 justify-center bg-opacity-90 backdrop-blur transition-shadow duration-100 [transform:translate3d(0,0,0)] shadow-sm z-40"
        ) as nav:
            with ui.nav().classes("bg-base-200"):
                with ui.element().classes("flex-1"):
                    with ui.label(for_=drawer.drawer_toggle).classes(f"btn drawer-button {self.hide_on}:hidden"):
                        ui.html(get_svg("menu"))
                with ui.element().classes(f"flex-none hidden {self.hide_on}:block"):
                    with ui.element("ul").classes("menu menu-horizontal menu-md"):
                        with ui.element("li"):
                            ui.link("Home", "/")
                        with ui.element("li"):
                            ui.link("Docs", "/docs")
                        with ui.element("li"):
                            ui.themeSelector()
