import io

import matplotlib.pyplot as plt
import seaborn as sns
import uvicorn

import src.ui as ui
from src.app import UiwizApp

app = UiwizApp()


def create_plot() -> str:
    sns.set_theme()
    tips = sns.load_dataset("tips")
    sns.relplot(
        data=tips,
        x="total_bill",
        y="tip",
        col="time",
        hue="smoker",
        style="smoker",
        size="size",
    )

    buf = io.BytesIO()
    plt.savefig(buf, format="svg")
    buf.seek(0)
    svg = buf.read().decode("utf-8")

    return svg


@app.page("/")
async def test():
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            ui.html(create_plot)


if __name__ == "__main__":
    uvicorn.run("seaborn_plot_example:app", reload=True)
