from io import BytesIO

import pandas as pd
import uvicorn
from fastapi import Request, UploadFile

import uiwiz.ui as ui
from uiwiz.app import UiwizApp

app = UiwizApp(theme="aqua")


def create_nav():
    with ui.nav():
        with ui.row():
            ui.button("this is from a method")
            ui.themeSelector()


@app.ui("/some/comnponent")
async def handle_upload(file: UploadFile):
    file_output = await file.read()
    df = pd.read_excel(BytesIO(file_output), engine="openpyxl")
    ui.table(df)


@app.page("/second")
async def test_2(request: Request):
    create_nav()
    with ui.element().classes(""):
        ui.label("second page")
        ui.link("page /", "/")

    with ui.footer():
        ui.label("some footer text")


code = """```python
class Test:
    def __init__(self):
        self.data = "asd"
```"""


@app.page("/")
async def test(request: Request):
    create_nav()
    with ui.col():
        ui.markdown(code)
        ui.link("some text", "/second").classes("btn")

        ui.upload(name="file").on_upload(on_upload=handle_upload, target=lambda: table.id)
        ui.checkbox("check")
        table = ui.table.from_dataframe(pd.DataFrame())
        ui.dropdown("select", ["item 1", "item 2"], "Pick item")
        ui.toggle("val")
        ui.toggle("val2", True)

        ui.divider()

    with ui.footer():
        ui.label("some footer text")


if __name__ == "__main__":
    uvicorn.run("run_simple:app", reload=True)
