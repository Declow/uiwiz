from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from typing_extensions import override

from uiwiz import PageDefinition, ui
from uiwiz.svg.svg_handler import get_svg

if TYPE_CHECKING:
    from collections.abc import Callable

parent = Path(__file__).parent
pages = []


class Page:
    def __init__(self, path: str, title: str, file: Path | str | Callable[[], str] | None = None) -> None:
        self.path = path
        self.title = title
        if isinstance(file, Path):
            with file.open("r") as f:
                self.content = f.read()
        elif isinstance(file, str) or callable(file):
            self.content = file
        else:
            self.content = None

        if path not in [page.path for page in pages]:
            pages.append(self)

    async def render(self) -> None:
        """Render the page content."""
        with ui.container(padding="p-4"):
            if callable(self.content):
                await self.content()
            else:
                ui.markdown(self.content)


Page(path="/", title="Home", file=parent / "pages/index.md")


class Layout(PageDefinition):
    def __init__(self) -> None:
        """Layout.

        A layout element that provides a consistent structure for the application.
        """
        super().__init__()
        self.drawer = None
        self._nav = None
        self.hide_on = "md"

    @override
    def content(self, _: ui.element) -> ui.element | None:
        self.drawer = ui.drawer()
        with self.drawer:
            with self.drawer.drawer_content() as content:
                self.nav(self.drawer)

            with self.drawer.drawer_side(), ui.element("ul").classes("flex-none block md:hidden w-full"):
                for page in pages:
                    with ui.element("li"):
                        ui.link(page.title, page.path)
                with ui.element("li"):
                    ui.themeSelector()

        return content

    @override
    def footer(self, _: ui.element) -> None:
        with ui.footer().classes("footer mx-auto footer-center p-4 text-base-content"):
            with ui.element("div").classes("flex flex-col items-center justify-center"):
                ui.label("Made with ❤️ by Uiwiz").classes("text-sm")
                ui.link("GitHub", "https://github.com/declow/uiwizard")

    def nav(self, drawer: ui.drawer) -> None:
        with ui.element().classes(
            "sticky top-0 flex h-16 justify-center bg-opacity-90 backdrop-blur transition-shadow duration-100 [transform:translate3d(0,0,0)] shadow-sm z-40",
        ):
            with ui.nav().classes("bg-base-200"):
                with ui.element().classes("flex-1"):
                    with ui.label(for_=drawer.drawer_toggle).classes(f"btn drawer-button {self.hide_on}:hidden"):
                        ui.html(get_svg("menu"))
                with ui.element().classes(f"flex-none hidden:{self.hide_on} block"):
                    with ui.element("ul").classes("menu menu-horizontal menu-md"):
                        for page in pages:
                            with ui.element("li"):
                                ui.link(page.title, page.path)
                        with ui.element("li"):
                            ui.themeSelector()
