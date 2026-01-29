from uiwiz import server

from multipage.second_page import router
from uiwiz import UiwizApp, ui

app = UiwizApp()
app.include_router(router)


@app.page("/")
async def test():
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            ui.element(content="Hello, world!")
            with ui.col():
                ui.link("Home", "/")
            with ui.col():
                ui.link("Second page", "/second_page")


if __name__ == "__main__":
    server.run("multipage.main:app")
