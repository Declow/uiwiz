import inspect
from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Any, Literal, Optional, Tuple, get_args, get_origin, get_type_hints

import uvicorn
from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefinedType

import uiwiz.ui as ui
from uiwiz.app import UiwizApp
from uiwiz.elements.form import UiAnno
from uiwiz.elements.label import Label
from uiwiz.elements.radio import Radio

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


switch = {
    str: ui.input,
    int: ui.input,
    float: ui.input,
    bool: ui.toggle,
    Literal: ui.dropdown,
    date: ui.datepicker,
    datetime: ui.datepicker,
}


def display_name(input: str) -> str:
    return input.replace("_", " ")


def render_element(
    ele: ui.element,
    field_class: type,
    key: str,
    placeholder: str,
    compact: bool,
    render_label: bool = True,
    classes: Optional[str] = None,
    value: Any = None,
) -> None:
    kwargs = {"name": key}
    if value:
        kwargs["value"] = value

    place = display_name(placeholder)
    label: Optional[Label] = None
    if render_label:
        if compact:
            if inspect.signature(ele).parameters.get("placeholder") is None:
                label = ui.label(place).classes("flex-auto w-24")
            else:
                kwargs["placeholder"] = place
        else:
            label = ui.label(place).classes("flex-auto w-36 font-bold")
    if field_class is Literal:
        print("field class is literal")
    el: ui.element = ele(**kwargs)
    if classes:
        el.classes(classes)
    if field_class is int:
        el.value = "0"
    if label:
        label.set_for(el)


def render_element_radio(field_class: type, key: str) -> None:
    for value in get_args(field_class):
        with ui.row():
            ui.element(content=display_name(value)).classes("flex-auto w-36 font-bold")
            ui.radio(name=key, value=value)


def render_element_dropdown(field_class: type, key: str, placeholder: Optional[str], compact: bool) -> None:
    if isinstance(placeholder, PydanticUndefinedType):
        placeholder = "---"
    if compact:
        ui.dropdown(key, get_args(field_class), placeholder)
    else:
        ui.element(content=display_name(key)).classes("flex-auto w-36 font-bold")
        ui.dropdown(key, get_args(field_class), placeholder)


def render_model(_type: BaseModel, compact: bool = True, **kwargs) -> None:
    if issubclass(_type, BaseModel) == False:
        raise ValueError("type must be a pydantic model")

    with ui.element().classes("card w-96 bg-base-100 shadow-md"):
        with ui.col():
            hints = get_type_hints(_type, include_extras=True)
            for key, field_type in hints.items():
                args = get_args(field_type)
                annotated = Annotated == get_origin(field_type)
                if key in kwargs:
                    render_key_override(key, **kwargs)
                else:
                    render_type_hint_without_args(args, annotated, ui.input, field_type, key, compact)
                    render_with_args_annotated(args, annotated, ui.toggle, _type, field_type, key, compact)
            ui.button("Save")


def render_key_override(key: str, **kwargs) -> None:
    if key in kwargs:
        args: dict = kwargs[key]
        model = args.pop("model")
        if not issubclass(model, ui.element):
            raise ValueError("type must be a ui element")
        if "name" not in args:
            args["name"] = key
        model(**args)
    else:
        raise ValueError("key not found in kwargs. Unable to render")


def render_type_hint_without_args(
    args: Tuple, annotated: bool, ele: ui.element, field_type, key, compact
) -> ui.element:
    if len(args) == 0:
        if annotated:
            render_element(switch.get(field_type), field_type, key, key, compact)

        render_element(switch.get(field_type), field_type, key, key, compact)


def render_with_args_annotated(
    args: Tuple, annotated: bool, ele: ui.element, _type: str, field_type: Tuple, key: str, compact: bool
) -> ui.element:
    if len(args) > 0:
        if annotated:
            field_type = args[0]
            for ele in args:
                if isinstance(ele, UiAnno):
                    render_label = False if ele.type is ui.hiddenInput else True
                    placeholder = ele.placeholder if ele.placeholder else key
                    if field_args := get_args(field_type):
                        for arg in field_args:
                            with ui.row():
                                render_element(
                                    ele.type,
                                    field_type,
                                    key,
                                    arg,
                                    compact,
                                    render_label,
                                    ele.classes,
                                    value=arg,
                                )
                    else:
                        render_element(ele.type, field_type, key, placeholder, compact, render_label, ele.classes)
        else:
            ele = switch.get(get_origin(field_type))
            if ele:
                render_element_dropdown(field_type, key, _type.model_fields[key].default, compact)


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
    with ui.form().on_submit(handle_submit) as form:
        render_model(DataInput, compact=False)
    with ui.form().on_submit(handle_submit) as form:
        render_model(DataInput, compact=True)

    with ui.form().on_submit(handle_submit) as form:
        render_model(
            DataInput,
            compact=True,
            id={"model": ui.input, "placeholder": 1},
            enum={
                "model": ui.dropdown,
                "items": ["asd", "ok", "values"],
            },
        )

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
        # create_display()
        create_form()


if __name__ == "__main__":
    uvicorn.run("validate_form_example:app", reload=True)
