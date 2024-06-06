from typing import Annotated

import uvicorn
from pydantic import BaseModel, Field

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.elements.form import FieldAnno

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


def render_model(klass: BaseModel):
    anno = klass.__annotations__
    for key, an in klass.__annotations__.items():
        for ele in an.__metadata__:
            placeholder = ele.placeholder if ele.placeholder else key
            ele.klass(name=key, placeholder=placeholder)
        # for ele in klass.__annotations__["name"].__metadata__:


class DataInput(BaseModel):
    name: Annotated[str, FieldAnno(klass=ui.input)] = Field(min_length=1)
    desc: Annotated[str, FieldAnno(klass=ui.textarea)] = Field(min_length=1)


def create_form():
    with ui.form().on_submit(handle_submit) as form:
        render_model(DataInput)
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
