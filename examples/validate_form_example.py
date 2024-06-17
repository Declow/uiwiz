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
    with ui.nav():
        ui.button("this is from a method")


class DataInput(BaseModel):
    id: Annotated[int, UiAnno(ui.hiddenInput)]
    enum: Literal["asd", "ok"]
    enum2: Annotated[Literal["asd", "ok"], UiAnno(ui.radio)] = "ok"
    only_str_defined: str
    name: Annotated[str, UiAnno(ui.input, "test")] = Field(min_length=1)
    desc: Annotated[str, UiAnno(ui.textarea)] = Field(min_length=1)
    age: Annotated[int, UiAnno(ui.input)] = Field(ge=0)
    is_active: bool = False
    event_at_date: date


def create_form():
    ui.modelForm(DataInput, compact=False).on_submit(handle_submit)
    ui.modelForm(DataInput, compact=True)

    ui.modelForm(
        DataInput,
        compact=True,
        id={"ui": ui.input, "placeholder": 1},
        enum={
            "ui": ui.dropdown,
            "items": ["asd", "ok", "values"],
        },
    ).on_submit(handle_submit)


@dataclass
class TestDataClasses:
    id: int
    name: str
    enum: Literal["asd", "ok"] = "ok"


def create_display():
    ins = DataInput(
        id=1, only_str_defined="test", name="test", desc="test", age=1, is_active=True, event_at_date=date.today()
    )
    # ui.show(ins)
    # ui.show(TestDataClasses(id=1, name="asdf"))
    # dic = {"id": 1, "name": "test", "enum": ["asd", "ok"], "test": {"test": "test"}}
    # ui.show(dic)
    # ui.show([ins,ins,ins,ins])
    # ui.show([dic,dic])


@app.ui("/handle/submit")
def handle_submit(data: DataInput):
    ui.toast("Data saved").success()
    print(data)


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
        # create_display()
        create_form()


if __name__ == "__main__":
    uvicorn.run("validate_form_example:app", reload=True)
