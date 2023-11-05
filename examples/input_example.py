from fastapi import Request
from pydantic import BaseModel
from uiwis.app import page, app
import uiwis.ui as ui
import uvicorn
import pandas as pd

app.setup()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")


class FormInput(BaseModel):
    first_name: str
    last_name: str


async def handle_input(data: FormInput):
    print(data)
    ui.toast("data saved")


@page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col"):
        with ui.form().on_submit(handle_input):
            ui.input("input name", "first_name")
            ui.input("input last name", "last_name")
            r = ui.radio("test-radio", "htmx")
            ui.label("Test for asd radio", r)
            ui.radio("test-radio", "javascript")
            ui.button("submit").attributes["type"] = "submit"


        ui.toastuigrid(pd.DataFrame(
                [
                    {"asd": 2},
                    {"asd": 3}
                ]
            )
        )
    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("input_example:app", reload=True)