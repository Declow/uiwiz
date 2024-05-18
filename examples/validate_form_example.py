import uvicorn
from pydantic import BaseModel, Field

import uiwiz.ui as ui
from uiwiz.app import UiwizApp

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


class DataInput(BaseModel):
    name: str = Field(min_length=1)
    desc: str = Field(min_length=1)


def create_form():
    with ui.form().on_submit(handle_submit) as form:
        ui.textarea("text", "desc")
        ui.input("text", "name")
        ui.button("Submit")

    return form


@app.ui("/handle/submit")
def handle_submit(data: DataInput):
    ui.toast("Data saved").success()


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col mx-auto"):
        create_form()


if __name__ == "__main__":
    uvicorn.run("validate_form_example:app", reload=True)
