import inspect
from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Any, Literal, TypedDict, TypeVar, Union, get_args, get_origin, get_type_hints

import uvicorn
from pydantic import BaseModel, Field

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.elements.form import UiAnno

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


switch = {
    str: ui.input,
    int: ui.input,
    float: ui.input,
    bool: ui.toggle,
    Literal: ui.radio,
    date: ui.datepicker,
    datetime: ui.datepicker,
}


def display_name(input: str) -> str:
    return input.replace("_", " ")


def render_element(
    ele: ui.element, field_class: type, key: str, placeholder: str, compact: bool, render_label=True
) -> None:
    kwargs = {"name": key}

    place = display_name(placeholder)
    if render_label:
        if compact:
            if inspect.signature(ele).parameters.get("placeholder") is None:
                ui.label(place)
            else:
                kwargs["placeholder"] = place
        else:
            ui.label(place).classes("font-bold")
    if field_class is Literal:
        print("field class is literal")
    el: ui.element = ele(**kwargs)
    if field_class is int:
        el.value = "0"


def render_element_radio(field_class: type, key: str) -> None:
    for value in get_args(field_class):
        with ui.row():
            ui.element(content=display_name(value)).classes("flex-auto w-36 font-bold")
            ui.radio(name=key, value=value)


def render_element_dropdown(field_class: type, key: str, compact: bool) -> None:
    if compact:
        ui.dropdown(key, get_args(field_class), "xxx")
    else:
        with ui.row():
            ui.element(content=display_name(key)).classes("flex-auto w-36 font-bold")
            ui.dropdown(key, get_args(field_class), "xxx")


def render_model(type: BaseModel, compact: bool = True) -> None:
    if issubclass(type, BaseModel) == False:
        raise ValueError("type must be a pydantic model")

    with ui.element().classes("card w-96 bg-base-100 shadow-md"):
        with ui.col():
            hints = get_type_hints(type, include_extras=True)
            for key, field_type in hints.items():
                args = get_args(field_type)
                annotated = Annotated == get_origin(field_type)
                # type_to_use = (
                #     switch.get(get_origin(field_type)) if switch.get(get_origin(field_type)) else switch.get(field_type)
                # )
                if len(args) == 0:
                    if annotated:
                        render_element(switch.get(field_type), field_type, key, key, compact)

                    render_element(switch.get(field_type), field_type, key, key, compact)
                else:
                    if annotated:
                        field_type = args[0]
                        for ele in args:
                            if isinstance(ele, UiAnno):
                                render_label = False if ele.type is ui.hiddenInput else True
                                placeholder = ele.placeholder if ele.placeholder else key
                                render_element(ele.type, field_type, key, placeholder, compact, render_label)
                    else:
                        ele = switch.get(get_origin(field_type))
                        if ele:
                            render_element_dropdown(field_type, key, compact)
                            # render_element_radio(field_type, key)
            ui.button("Save")


class DataInput(BaseModel):
    id: Annotated[int, UiAnno(ui.hiddenInput)]
    enum: Literal["asd", "ok"] = "ok"
    only_str_defined: str
    name: Annotated[str, UiAnno(ui.input, "test")] = Field(min_length=1)
    desc: Annotated[str, UiAnno(ui.textarea)] = Field(min_length=1)
    age: Annotated[int, UiAnno(ui.input)] = Field(ge=0)
    is_active: bool = False
    event_at_date: date


def create_form():
    with ui.form().on_submit(handle_submit) as form:
        render_model(DataInput, compact=False)
    with ui.form().on_submit(handle_submit) as form:
        render_model(DataInput, compact=True)

    return form


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
        create_display()
        create_form()


if __name__ == "__main__":
    uvicorn.run("validate_form_example:app", reload=True)
