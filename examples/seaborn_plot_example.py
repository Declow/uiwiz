import seaborn as sns
import matplotlib.pyplot as plt
from fastapi import Request, UploadFile
from uiwiz.app import UiwizApp
import uiwiz.ui as ui
import uvicorn
import pandas as pd
import io

app = UiwizApp()

def create_plot() -> str:
    sns.set_theme()
    tips = sns.load_dataset("tips")
    sns.relplot(
        data=tips,
        x="total_bill", y="tip", col="time",
        hue="smoker", style="smoker", size="size",
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