from typing import Optional

import pandas as pd
import uvicorn
from fastapi import Request
from pydantic import BaseModel, ValidationError

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.element import Element

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


class DataInput(BaseModel):
    name: str
    desc: str


def create_form(swap: Optional[str] = None, input: DataInput = None):
    invalid = False
    with ui.form().on_submit(handle_submit, swap=swap) as form:
        name = ui.input("text", "name")
        desc = ui.textarea("text", "desc")
        ui.button("Submit")
        if input:
            if input.name == "":
                name.classes(ui.input._classes + " invalid")
                invalid = True
            else:
                name.value = input.name

            if input.desc == "":
                desc.classes(ui.input._classes + " invalid")
                invalid = True
            else:
                desc.content = input.desc

    form.event["target"] = form
    return form, invalid


@app.ui("/handle/submit")
def handle_submit(data: DataInput):
    form, invalid = create_form(input=data)
    with form:
        if invalid:
            ui.toast("Missing field").error()
        else:
            ui.toast("Data saved").success()


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col mx-auto"):
        create_form("outerHTML")


if __name__ == "__main__":
    uvicorn.run("validate_form_example:app", reload=True)
