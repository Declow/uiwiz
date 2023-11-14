from fastapi import Request
from pydantic import BaseModel
from uiwiz.app import UiwizApp
from uiwiz.element import Element
import uiwiz.ui as ui
import uvicorn
import pandas as pd

app = UiwizApp()

df = pd.DataFrame([{
                "col1": "val1",
                "col2": "val2",
                "col3": "val1",
                "col4": "val1asdsadasds",
                "col5": "val1",
                "col6": "val1",
                "col7": "val1",
                "col8": "val1",
                "col9": "val1",
                "col10": "val1",
                "col21": "val2",
                "col31": "val1",
                "col41": "val1asdsadasds",
                "col51": "val1",
                "col61": "val1",
                "col71": "val1",
                "col81": "val1",
                "col91": "val1",
            }, {
                "col1": "val1",
                "col2": "val2",
                "col3": "val1",
                "col4": "val1",
                "col5": "val1",
                "col6": "val1",
                "col7": "val1",
                "col8": "val1",
                "col9": "val1",
                "col10": "val1",
                "col21": "val2",
                "col31": "val1",
                "col41": "val1asdsadasds",
                "col51": "val1",
                "col61": "val1",
                "col71": "val1",
                "col81": "val1",
                "col91": "val1",
            }, {
                "col1": "val1",
                "col2": "val2",
                "col3": "val1",
                "col4": "val1",
                "col5": "val1",
                "col6": "val1",
                "col7": "val1",
                "col8": "val1",
                "col9": "val1",
                "col10": "val1",
                "col21": "val2",
                "col31": "val1",
                "col41": "val1asdsadasds",
                "col51": "val1",
                "col61": "val1",
                "col71": "val1",
                "col81": "val1",
                "col91": "val1",
            }])

def create_nav():
    with ui.nav():
        ui.button("this is from a method")

def e():
    ui.label("new label from htmx")

async def create_from_htmx(b: ui.button):
    with ui.label("This label came from htmx aka the server"):
        ui.label("Text from button " + b.content)

def create_label(message):
    ui.label(message)

async def update_res(request: Request, message: str):
    data = await request.json()
    create_label(f'{message} {data.get("input")}')

class DataInput(BaseModel):
    input: str

@app.page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col mx-auto"):
        with ui.row():
            ui.button("test").on_click(lambda: create_from_htmx(b), endpoint="/endpoint")
            b = ui.button("asd").on_click(e)

            ui.button("Add toast").on_click(lambda: ui.toast("this is a toast very long toast"), swap="beforeend").classes("btn")
            
            ui.markdown('''This is **Markdown**.''')
        ui.markdown("""```python
if True:
    print("hi")
```""")

        message = "New content:"
        def replace(request: Request, input: DataInput):
            create_label(f'{message} {input.input}')
            
        ui.input("This is a placeholder", name="input", on_change=replace, target=lambda: res3.id)
        with Element() as res3:
            create_label(message)

        ui.textarea("Placeholder", name="input", on_change=replace, target=lambda: res2.id, trigger="input, keyup[(ctrlKey||metaKey)&&keyCode==13]")
        res2 = ui.label(message)

        ui.table(df)
        ui.aggrid(df)



    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run:app", reload=True)