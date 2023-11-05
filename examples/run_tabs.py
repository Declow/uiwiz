from fastapi import Request
from uiwis.app import page, app
import uiwis.ui as ui
import uvicorn

app.setup()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")


@page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col"):
        with ui.tabs() as tabs:
            one = ui.tab("Tab 1")
            two = ui.tab("Tab 2")
        with ui.tab_panels(tabs, two):
            with ui.tab_panel(one):
                ui.label("1")
            with ui.tab_panel(two):
                ui.label("2")
        
        ui.label("This is outside of tabs")

        with ui.tabs() as tabs:
            one = ui.tab("Tab 1")
            two = ui.tab("Tab 2")
        with ui.tab_panels(tabs, one):
            with ui.tab_panel(one):
                ui.toastuigrid(None)
            with ui.tab_panel(two):
                ui.label("2")
        

    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run_tabs:app", reload=True)