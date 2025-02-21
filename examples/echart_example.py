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
        ui.markdown(
            """# EChart Example
This is an example of EChart component.
        """
        )
        EChart(
            {
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "line"}},
                "xAxis": {
                    "type": "category",
                    "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                },
                "yAxis": {"type": "value"},
                "series": [
                    {
                        "name": "Sales",
                        "type": "line",
                        "data": [150, 230, 224, 218, 135, 147, 260],
                    }
                ],
            }
        )


if __name__ == "__main__":
    uvicorn.run("echart_example:app", reload=True)
