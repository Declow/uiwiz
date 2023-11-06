from fastapi import Request
from pydantic import BaseModel
from uiwiz.app import page, app
import uiwiz.ui as ui
import uvicorn
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


class FormInput(BaseModel):
    first_name: str
    last_name: str


async def handle_input(data: FormInput):
    ui.toast("data saved")


@page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col"):
        with ui.form().on_submit(handle_input):
            ui.input("input name", "first_name")
            la_name = ui.input("input last name", "last_name")
            ui.label().bind_text_from(la_name, "last_name", "input")
            r = ui.radio("test-radio", "htmx")
            ui.label("Test for asd radio", r)
            ui.radio("test-radio", "javascript")
            range = ui.range(0, 100, 0, "value")
            ui.label(range.value).bind_text_from(range, "value", "input delay:20ms")
            ui.button("submit").attributes["type"] = "submit"


        ui.toastuigrid(pd.DataFrame(
                [
                    {"asd": 2},
                    {"asd": 3}
                ]
            )
        )
        range = ui.range(0, 100, 0, "value")
        ui.label(range.value).bind_text_from(range, "value")
    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("input_example:app", reload=True)