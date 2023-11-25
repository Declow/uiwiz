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
            with ui.tabs().classes("tabs justify-center") as tabs:
                one = ui.tab("Tab 1")
                two = ui.tab("Tab 2")
            with ui.tab_panels(tabs, two):
                with ui.tab_panel(one):
                    ui.label("1")
                with ui.tab_panel(two):
                    ui.label("2")
            
            ui.divider()
            ui.label("This is outside of tabs")
            ui.divider()

            with ui.tabs() as tabs:
                one = ui.tab("Tab 1")
                two = ui.tab("Tab 2")
            with ui.tab_panels(tabs, one):
                with ui.tab_panel(one):
                    ui.aggrid(pd.DataFrame([{"asd": 1}]))
                with ui.tab_panel(two):
                    ui.label("2")
            

    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run_tabs:app", reload=True)