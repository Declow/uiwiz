import os
from datetime import date
from typing import Annotated, Literal

import uvicorn
from fastapi_profiler import PyInstrumentProfilerMiddleware
from pydantic import BaseModel, Field

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.models.model_handler import UiAnno

app = UiwizApp(auto_close_toast_error=False)
app.add_middleware(
    PyInstrumentProfilerMiddleware,
    server_app=app,  # Required to output the profile on server shutdown
    profiler_output_type="html",
    is_print_each_request=False,  # Set to True to show request profile on
    # stdout on each request
    open_in_browser=False,  # Set to true to open your web-browser automatically
    # when the server shuts down
    html_file_name="example_profile.html",  # Filename for output
)


def create_nav():
    with ui.nav().classes("bg-neutral shadow-xl"):
        ui.button("this is from a method")


class DataInput(BaseModel):
    enum: Literal["val", "ok"]
    only_str_defined: str
    name: Annotated[str, UiAnno(ui.input, "test")] = Field(min_length=1)
    desc: Annotated[str, UiAnno(ui.textarea)] = Field(min_length=1)
    age: Annotated[int, UiAnno(ui.input)] = Field(ge=0)
    is_active: bool = False
    event_at_date: date
    test: int


class DataInputWithId(DataInput):
    id: Annotated[int, UiAnno(ui.hiddenInput)]
    enum: Literal["val", "ok"]
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
        DataInputWithId,
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
    instance = DataInputWithId(
        id=1,
        enum="val",
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
    with ui.col().classes("lg:px-80"):
        create_form()


if __name__ == "__main__":
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(app=f"{app_name}:app", host="0.0.0.0", port=8080, workers=1)
