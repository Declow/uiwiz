from dataclasses import dataclass
from datetime import date, datetime
import inspect
from typing import Annotated, Any, Callable, Literal, Optional, Tuple, Union, get_args, get_origin, get_type_hints

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

    def __init__(self, model: BaseModel, compact: bool = True):
        self.model = model
        self.compact = compact
        self.render_model(
            model,
        )
        self.button.render_html = False

    def on_submit(self, *args, **kwargs) -> None:
        self.button.render_html = True
        self.form.on_submit(*args, **kwargs)
        return self

    def render_element(
        self,
        ele: Element,
        field_class: type,
        key: str,
        placeholder: str,
        render_label: bool = True,
        classes: Optional[str] = None,
        value: Any = None,
    ) -> None:
        kwargs = {"name": key}
        if value:
            kwargs["value"] = value

        place = __display_name__(placeholder)
        label: Optional[Label] = None
        if render_label:
            if self.compact:
                if inspect.signature(ele).parameters.get("placeholder") is None:
                    label = Label(place).classes("flex-auto w-24")
                else:
                    kwargs["placeholder"] = place
            else:
                label = Label(place).classes("flex-auto w-36 font-bold")
        if field_class is Literal:
            print("field class is literal")
        el: Element = ele(**kwargs)
        if classes:
            el.classes(classes)
        if field_class is int:
            el.value = "0"
        if label:
            label.set_for(el)

    def render_element_radio(self, field_class: type, key: str) -> None:
        for value in get_args(field_class):
            with Row():
                Element(content=__display_name__(value)).classes("flex-auto w-36 font-bold")
                Radio(name=key, value=value)

    def render_element_dropdown(self, field_class: type, key: str, placeholder: Optional[str]) -> None:
        if isinstance(placeholder, PydanticUndefinedType):
            placeholder = "---"
        if self.compact:
            Dropdown(key, get_args(field_class), placeholder)
        else:
            Element(content=__display_name__(key)).classes("flex-auto w-36 font-bold")
            Dropdown(key, get_args(field_class), placeholder)

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
                        self.render_key_override(key, **kwargs)
                    else:
                        self.render_type_hint_without_args(args, annotated, field_type, key)
                        self.render_with_args_annotated(args, annotated, _type, field_type, key)
                self.button = Button("Save")
        self.form = form

    def render_key_override(self, key: str, **kwargs) -> None:
        if key in kwargs:
            args: dict = kwargs[key]
            model = args.pop("model")
            if not issubclass(model, Element):
                raise ValueError("type must be a ui element")
            if "name" not in args:
                args["name"] = key

            model(**args)
        else:
            raise ValueError("key not found in kwargs. Unable to render")

    def render_type_hint_without_args(self, args: Tuple, annotated: bool, field_type, key) -> Element:
        if len(args) == 0:
            if annotated:
                self.render_element(switch.get(field_type), field_type, key, key, self.compact)

            self.render_element(switch.get(field_type), field_type, key, key, self.compact)

    def render_with_args_annotated(
        self, args: Tuple, annotated: bool, _type: str, field_type: Tuple, key: str
    ) -> Element:
        if len(args) > 0:
            if annotated:
                field_type = args[0]
                for ele in args:
                    if isinstance(ele, UiAnno):
                        render_label = False if ele.type is HiddenInput else True
                        placeholder = ele.placeholder if ele.placeholder else key
                        if field_args := get_args(field_type):
                            for arg in field_args:
                                with Row():
                                    self.render_element(
                                        ele.type,
                                        field_type,
                                        key,
                                        arg,
                                        render_label,
                                        ele.classes,
                                        value=arg,
                                    )
                        else:
                            self.render_element(ele.type, field_type, key, placeholder, render_label, ele.classes)
            else:
                ele = switch.get(get_origin(field_type))
                if ele:
                    self.render_element_dropdown(field_type, key, _type.model_fields[key].default)
