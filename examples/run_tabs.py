from fastapi import Request
from uiwiz.app import UiwizApp
import uiwiz.ui as ui
import uvicorn
import pandas as pd

app = UiwizApp()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")


@app.page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            with ui.tabs() as tu:
                with ui.tab("Content 1"):
                    ui.label("asd")
                with ui.tab("Content 2"):
                    with ui.col():
                        ui.label("asd2")
                        ui.label("asd2")
                        ui.label("asd2")
                        ui.label("asd2")
                        ui.label("asd2")
                with ui.tab("This is 3").active():
                    ui.label("cccxxx3")
                    ui.spinner().infinity()

            ui.divider()
            ui.label("This is outside of tabs")
            ui.divider()


            print(tu)
            

    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run_tabs:app", reload=True)