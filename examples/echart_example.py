import uvicorn

from uiwiz import UiwizApp, ui
from uiwiz.elements.echart.echart import EChart
app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.themeSelector()


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
        EChart()


if __name__ == "__main__":
    uvicorn.run("echart_example:app", reload=True)
