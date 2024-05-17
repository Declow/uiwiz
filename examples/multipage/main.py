from uiwiz import UiwizApp, ui
import uvicorn
from examples.multipage.second_page import router

app = UiwizApp()
app.add_page_router(router)

@app.page("/")
async def test():
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            ui.element(content="Hello, world!")
            for route in router.paths.keys():
                ui.link(route, route)

if __name__ == "__main__":
    uvicorn.run("examples.multipage.main:app", reload=True, port=8000)