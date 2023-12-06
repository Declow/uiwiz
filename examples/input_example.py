from typing import Optional
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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    asd: Optional[str] = None
    value: Optional[str] = None
    test_radio: Optional[str] = None


async def handle_input(data: FormInput):
    with ui.element():
        ui.label("outside of oob")
        with ui.element():
            ui.label("test")
            with ui.element():
                ui.label("test")
        with ui.toast().info():
            with ui.element().classes("col"):
                ui.label("test in")
                ui.label("test insob")
        ui.label("outside of oob below")
    await asyncio.sleep(1)
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

                with ui.row():
                    r = ui.radio("test_radio", "htmx")
                    ui.label("htmx", r)
                with ui.row():
                    r1 = ui.radio("test_radio", "javascript")
                    ui.label("javascript", r1)
                range2 = ui.range(0, 100, 0, "value")
                ui.label(range2.value).bind_text_from(range2)
                with ui.row():
                    b = ui.button("submit")
                    ui.spinner(b).ring().large()
            with ui.form().on_submit(handle_input):
                with ui.button("submit2") as b2:
                    ui.spinner(b2).ring().large()
                
                ui.html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>')

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