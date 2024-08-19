from dataclasses import dataclass
from datetime import date
from typing import Annotated, Literal

import uvicorn
from pydantic import BaseModel, Field

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.model_handler import UiAnno

app = UiwizApp()


def create_nav():
    with ui.nav().classes("bg-neutral shadow-xl"):
        ui.button("this is from a method")


class DataInput(BaseModel):
    id: Annotated[int, UiAnno(ui.hiddenInput)]
    enum: Literal["val", "ok"]
    enum2: Annotated[Literal["asd", "ok"], UiAnno(ui.radio)] = "asd"
    only_str_defined: str
    name: Annotated[str, UiAnno(ui.input, "test")] = Field(min_length=1)
    desc: Annotated[str, UiAnno(ui.textarea)] = Field(min_length=1)
    age: Annotated[int, UiAnno(ui.input)] = Field(ge=0)
    is_active: bool = False
    event_at_date: date
    test: int


def create_form():
    ui.modelForm(DataInput, compact=False).on_submit(handle_submit)
    ui.modelForm(DataInput, compact=True)  # Missing on submit. No button is created

    # Customizing the form
    # Override the annotation for the name field
    ui.modelForm(
        DataInput,
        compact=True,
        id={"ui": ui.input, "value": 1},
        enum={
            "ui": ui.dropdown,
            "placeholder": "Select",
            "items": ["asd", "ok", "values"],
        },
    ).on_submit(handle_submit)

    # Using the instance
    # This will prefill the form with the instance data
    instance = DataInput(
        id=1,
        enum="val",
        enum2="asd",
        only_str_defined="asd",
        name="test",
        desc="This is a test",
        age=1,
        is_active=True,
        event_at_date=date.today(),
        test=10,
    )
    ui.modelForm(
        instance, compact=False, test={"ui": ui.dropdown, "placeholder": "Select", "items": [1, 2, 3, 4]}
    ).on_submit(handle_submit)


@app.ui("/handle/submit")
def handle_submit(data: DataInput):
    ui.toast("Data saved").success()
    print(data)


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
        create_form()


if __name__ == "__main__":
    uvicorn.run("validate_form_example:app", reload=True)
