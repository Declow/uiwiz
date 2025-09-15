import logging

import uvicorn

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.svg.svg_handler import get_svg

logging.basicConfig(level=logging.INFO)

app = UiwizApp(theme="nord")


@app.page("/drawer-2")
async def test():
    with ui.drawer() as drawer:
        with drawer.drawer_content():
            with ui.element().classes(
                "sticky top-0 flex h-16 justify-center bg-opacity-90 backdrop-blur transition-shadow duration-100 [transform:translate3d(0,0,0)] shadow-sm"
            ):
                with ui.nav():
                    drawer.drawer_button()

            with ui.col():
                ui.label("test1")
                ui.button("Click me")
                ui.label("test1")

            with ui.footer():
                ui.label("some footer text")

        with drawer.drawer_side():
            with ui.element("li"):
                ui.link("Drawer-1", "/")
            ui.link("Some link", "https://google.com")


@app.page("/")
async def test():
    with ui.drawer(always_open=True, right=False) as drawer:
        with drawer.drawer_content():
            with ui.element().classes(
                "sticky top-0 flex h-16 justify-center bg-opacity-90 backdrop-blur transition-shadow duration-100 [transform:translate3d(0,0,0)] shadow-sm"
            ):
                with ui.nav().classes("w-full navbar"):
                    with ui.label(for_=drawer.drawer_toggle).classes("btn drawer-button lg:hidden"):
                        ui.html(get_svg("menu"))

            ui.label("test1")
            with ui.footer():
                ui.label("some footer text")

        with drawer.drawer_side():
            with ui.element("li"):
                ui.link("drawer-2", "/drawer-2")
                ui.link("Some link", "https://google.com")


if __name__ == "__main__":
    uvicorn.run("drawer_example:app", reload=True)
