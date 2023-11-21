from typing import Optional
from fastapi import Request
from pydantic import BaseModel
from uiwiz.app import UiwizApp
import uiwiz.ui as ui
import uvicorn
import pandas as pd
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

app = UiwizApp()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")


class FormInput(BaseModel):
    first_name: str
    last_name: str
    asd: Optional[str]
    value: Optional[str]


async def handle_input(data: FormInput):
    ui.toast("data saved")
    await asyncio.sleep(2)
    print(data)


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            with ui.form().on_submit(handle_input):
                ui.input("input name", "first_name")
                la_name = ui.input("input last name", name="last_name")
                ui.label().bind_text_from(la_name)

                text = ui.textarea(name="asd")
                ui.label().bind_text_from(text)

                r = ui.radio("test-radio", "htmx")
                ui.label("Test for asd radio", r)
                ui.radio("test-radio", "javascript")
                range2 = ui.range(0, 100, 0, "value")
                ui.label(range2.value).bind_text_from(range2)
                with ui.row():
                    with ui.button("submit") as b:
                        ui.spinner(b).ring().large()
                

                ui.spinner().ring().extra_small()
                ui.spinner().ball().large()

                ui.aggrid(pd.DataFrame(
                        [
                            {"asd": 2, "kek": "val", "kek2": "val", "kek3": "val", "kek very long column": "val", "kek very long column2": "val", "kek very long column3": "val"},
                            {"asd": 3, "kek": "val"}
                        ]
                    ))
                range = ui.range(0, 100, 0, "value2")
                ui.label(range.value).bind_text_from(range)

    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("input_example:app", reload=True)