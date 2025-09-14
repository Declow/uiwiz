import uvicorn

import src.ui as ui
from src.app import UiwizApp

app = UiwizApp()


def create_nav():
    with ui.nav().classes("bg-base-200"):
        ui.button("this is from a method")


@app.page("/")
async def test():
    create_nav()
    with ui.container():
        with ui.element().classes("w-full"):
            with ui.tabs() as tu:
                with ui.tab("Content 1"):
                    ui.label("asd")
                with ui.tab("Content 2"):
                    with ui.col():
                        ui.label("asd2")
                with ui.tab("This is 3").active():
                    ui.label("cccxxx3")
                    ui.spinner().infinity()

            ui.divider("xx")
            ui.label("This is outside of tabs")
            ui.divider()

    with ui.footer():
        ui.label("some footer text")


if __name__ == "__main__":
    uvicorn.run("run_tabs:app", reload=True)
