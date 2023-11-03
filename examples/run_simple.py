from pathlib import Path
from fastapi import Request, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from uiwis.app import page, app
from uiwis.element import Element
import uiwis.ui as ui
import uvicorn
import pandas as pd

app.setup()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")

async def handle_upload_2(file: UploadFile, table_id: str):
    file_output = await file.read()
    df = pd.read_excel(file_output, engine="openpyxl")
    ui.toastuigrid(df, id=table_id)

@page("/second")
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

@page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col"):
        ui.markdown(code)
        ui.link("some text", "/second")
        async def handle_upload(file: UploadFile):
            await handle_upload_2(file, table.id)
        ui.upload(on_upload=handle_upload, target=lambda: table.id)
        ui.checkbox("check")
        table = ui.toastuigrid(None)
        ui.dropdown(["item 1", "item 2"], "Pick item")
        ui.toggle("val")
        ui.toggle("val2", True)

        ui.code(code)

    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run_simple:app", reload=True)