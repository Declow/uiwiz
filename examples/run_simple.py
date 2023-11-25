from fastapi import Request, UploadFile
from uiwiz.app import UiwizApp
import uiwiz.ui as ui
import uvicorn
import pandas as pd

app = UiwizApp()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")

async def handle_upload_2(file: UploadFile, table_id: str):
    file_output = await file.read()
    df = pd.read_excel(file_output, engine="openpyxl")

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
    with ui.element().classes("col"):
        ui.markdown(code)
        ui.link("some text", "/second").classes("btn")
        async def handle_upload(file: UploadFile):
            await handle_upload_2(file, table.id)
        ui.upload(on_upload=handle_upload, target=lambda: table.id)
        ui.checkbox("check")
        table = ui.table(None)
        ui.dropdown(["item 1", "item 2"], "Pick item")
        ui.toggle("val")
        ui.toggle("val2", True)

        ui.divider()

        ui.code(code)

    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run_simple:app", reload=True)