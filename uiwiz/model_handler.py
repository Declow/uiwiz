import inspect
from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Any, Literal, Optional, Tuple, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType

from uiwiz.element import Element
from uiwiz.elements.button import Button
from uiwiz.elements.checkbox import Checkbox
from uiwiz.elements.col import Col
from uiwiz.elements.datepicker import Datepicker
from uiwiz.elements.dropdown import Dropdown
from uiwiz.elements.form import Form
from uiwiz.elements.hidden_input import HiddenInput
from uiwiz.elements.input import Input
from uiwiz.elements.label import Label
from uiwiz.elements.radio import Radio
from uiwiz.elements.row import Row
from uiwiz.elements.textarea import TextArea
from uiwiz.elements.toggle import Toggle
from uiwiz.show import __display_name__


@dataclass
class UiAnno:
    type: Union[Input, TextArea, Checkbox] = None
    placeholder: Optional[str] = None
    classes: Optional[str] = None


switch = {
    str: Input,
    int: Input,
    float: Input,
    bool: Toggle,
    Literal: Dropdown,
    date: Datepicker,
    datetime: Datepicker,
}


class ModelForm:
    model: BaseModel
    compact: bool
    form: Form
    button: Button

    def __init__(self, model: BaseModel, compact: bool = True, **kwargs):
        self.model = model
        self.compact = compact
        self.render_model(model, **kwargs)
        self.button.render_html = False

    def on_submit(self, *args, **kwargs) -> None:
        self.button.render_html = True
        self.form.on_submit(*args, **kwargs)
        return self

    def render_model(self, _type: BaseModel, **kwargs) -> None:
        """
        Why give the on submit function as a parameter?
        The renderere needs to know if the save should be created or not.
        """
        if issubclass(_type, BaseModel) == False:
            raise ValueError("type must be a pydantic model")

        with Form().classes("card w-96 bg-base-100 shadow-md") as form:
            with Col():
                hints = get_type_hints(_type, include_extras=True)
                for key, field_type in hints.items():
                    args = get_args(field_type)
                    annotated = Annotated == get_origin(field_type)
                    if key in kwargs:
                        self.render_key_override(key, field_type, **kwargs)
                    else:
                        self.render_type_hint_without_args(args, annotated, field_type, key)
                        self.render_with_args_annotated(args, annotated, _type, field_type, key)
                self.button = Button("Save")
        self.form = form

    def render_key_override(self, key: str, field_type: type, **kwargs) -> None:
        if key in kwargs:
            args: dict = kwargs[key]
            model = args.pop("ui")
            if not issubclass(model, Element):
                raise ValueError("type must be a ui element")
            if "name" not in args:
                args["name"] = key

            model(**args)

            # self.render_element(
            #     model,
            #     field_type,
            #     key,
            # )
        else:
            raise ValueError("key not found in kwargs. Unable to render")

    def render_type_hint_without_args(self, args: Tuple, annotated: bool, field_type, key) -> Element:
        if len(args) == 0:
            if annotated:
                self.render_element(switch.get(field_type), field_type, key, key)

            self.render_element(switch.get(field_type), field_type, key, key)

    def render_with_args_annotated(
        self, args: Tuple, annotated: bool, _type: BaseModel, field_type: Tuple, key: str
    ) -> Element:
        if len(args) > 0:
            if annotated:
                field_type = args[0]
                for ele in args:
                    if isinstance(ele, UiAnno):
                        placeholder = ele.placeholder if ele.placeholder else key
                        if field_args := get_args(field_type):
                            self.render_element_radio(ele, field_type, key, field_args)
                        else:
                            self.render_element(ele.type, field_type, key, placeholder, ele.classes)
            else:
                ele = switch.get(get_origin(field_type))
                if ele:
                    self.render_element_dropdown(field_type, key, _type.model_fields[key].default)

    def render_element(
        self,
        ele: Element,
        field_class: type,
        key: str,
        placeholder: str,
        classes: Optional[str] = None,
        value: Any = None,
        **kwargs,
    ) -> None:
        kwargs = {**{"name": key}, **kwargs}
        if value:
            kwargs["value"] = value

        place = __display_name__(placeholder)
        label: Optional[Label] = None
        if ele is not HiddenInput:
            label = Label(place).classes("flex-auto w-36 font-bold")

            if self.compact and inspect.signature(ele).parameters.get("placeholder"):
                label.render_html = False
                kwargs["placeholder"] = place
            else:
                label.classes("flex-auto w-24")
                label.render_html = True

        el: Element = ele(**kwargs)
        if classes:
            el.classes(classes)
        if field_class is int:
            el.value = "0"
        if label:
            label.set_for(el)

    # def create_kwargs(self, key: str, placeholder: str, value: str, **kwargs) -> dict:
    #     __kwargs = {**{"name": key, "placeholder": placeholder, "value": value}, **kwargs}
    #     print(__kwargs)
    #     return __kwargs

    def render_element_radio(
        self,
        ele: UiAnno,
        field_class: type,
        key: str,
        field_args: Tuple,
    ) -> None:
        for arg in field_args:
            with Row():
                self.render_element(
                    Radio,
                    field_class,
                    key,
                    arg,
                    ele.classes,
                    value=arg,
                )

    def render_element_dropdown(self, field_class: type, key: str, placeholder: Optional[str]) -> None:
        if isinstance(placeholder, PydanticUndefinedType):
            placeholder = __display_name__(key)

        self.render_element(Dropdown, field_class, key, placeholder, items=get_args(field_class))
