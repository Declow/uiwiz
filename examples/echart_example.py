from random import randint

import uvicorn

from uiwiz import UiwizApp, ui

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.themeSelector()


@app.post("/update/chart")
async def update_chart():
    return ui.echart.response(
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
                    "data": [randint(0, 300) for _ in range(7)],
                }
            ],
        }
    )


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
        ui.markdown(
            """# EChart Example
This is an example of EChart component.
        """
        )
        ui.button("Update Chart").on_click(update_chart, lambda: chart.id, swap="none")
        chart = ui.echart(
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

        ui.markdown("## Sankey Chart")
        ui.echart(
            {
                "series": {
                    "type": "sankey",
                    "layout": "none",
                    "emphasis": {"focus": "adjacency"},
                    "data": [
                        {"name": "a"},
                        {"name": "b"},
                        {"name": "a1"},
                        {"name": "a2"},
                        {"name": "b1"},
                        {"name": "c"},
                    ],
                    "links": [
                        {"source": "a", "target": "a1", "value": 5},
                        {"source": "a", "target": "a2", "value": 3},
                        {"source": "b", "target": "b1", "value": 8},
                        {"source": "a", "target": "b1", "value": 3},
                        {"source": "b1", "target": "a1", "value": 1},
                        {"source": "b1", "target": "c", "value": 2},
                    ],
                }
            }
        )


if __name__ == "__main__":
    uvicorn.run("echart_example:app", reload=True)
