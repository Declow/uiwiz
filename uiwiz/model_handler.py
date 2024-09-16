import inspect
from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Literal, Optional, Tuple, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType

from uiwiz.element import Element
from uiwiz.elements.button import Button
from uiwiz.elements.checkbox import Checkbox
from uiwiz.elements.datepicker import Datepicker
from uiwiz.elements.divider import Divider
from uiwiz.elements.dropdown import Dropdown
from uiwiz.elements.form import Form
from uiwiz.elements.hidden_input import HiddenInput
from uiwiz.elements.input import Input
from uiwiz.elements.label import Label
from uiwiz.elements.radio import Radio
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
    label_classes: str
    instance: Optional[BaseModel]

    def __init__(
        self,
        model: BaseModel,
        compact: bool = True,
        card_classes: str = "card w-full bg-base-100 shadow-lg",
        label_classes: str = "flex-auto w-52",
        **kwargs,  # override fields with custom ui
    ):
        self.model = model
        self.instance = None

        if isinstance(model, BaseModel):
            self.model = model.__class__
            self.instance = model
        self.compact = compact
        self.label_classes = label_classes
        self.card_classes = card_classes
        self.render_model(**kwargs)
        self.button.render_html = False

    def on_submit(self, *args, **kwargs) -> "ModelForm":
        self.button.render_html = True
        self.form.on_submit(*args, **kwargs)
        return self

    def render_model(self, **kwargs) -> Form:
        if issubclass(self.model, BaseModel) == False:
            raise ValueError("type must be a pydantic model")

        with Form().classes(self.card_classes) as form:
            hints = get_type_hints(self.model, include_extras=True)
            for key, field_type in hints.items():
                args = get_args(field_type)
                annotated = Annotated == get_origin(field_type)
                if key in kwargs:
                    self.render_key_override(args, key, field_type, **kwargs)
                else:
                    self.render_type_hint_without_args(args, annotated, field_type, key)
                    self.render_with_args_annotated(args, annotated, field_type, key)
            self.button = Button("Save")
        self.form = form

    def render_key_override(self, args: Tuple, key: str, field_type: type, **kwargs) -> None:
        if key in kwargs:
            model_args: dict = kwargs[key]
            model = model_args.pop("ui")
            placeholder = str(model_args.pop("placeholder", key))
            if not issubclass(model, Element):
                raise ValueError("type must be type of Element")
            if "name" not in model_args:
                model_args["name"] = key

            _, arg = self.get_type_and_uianno(args)
            classes = None
            if arg:
                classes = arg.classes
            self.render_element(model, key, classes, placeholder=placeholder, **model_args)
        else:
            raise ValueError("key not found in kwargs. Unable to render")

    def render_type_hint_without_args(self, args: Tuple, annotated: bool, field_type, key) -> Element:
        if len(args) == 0:
            if annotated:
                self.render_element(switch.get(field_type), key, placeholder=key)

            self.render_element(switch.get(field_type), key, placeholder=key)

    def render_with_args_annotated(self, args: Tuple, annotated: bool, field_type: Tuple, key: str) -> Element:
        if len(args) > 0:
            if annotated:
                field_type, ele = self.get_type_and_uianno(args)
                if ele:
                    placeholder = ele.placeholder if ele.placeholder else key
                    if field_args := get_args(field_type):
                        self.render_element_radio(ele, key, field_args)
                    else:
                        self.render_element(ele.type, key, ele.classes, placeholder=placeholder)
            else:
                ele = switch.get(get_origin(field_type))
                if ele:
                    self.render_element_dropdown(field_type, key, self.model.model_fields[key].default)

    def get_type_and_uianno(self, args: Tuple) -> Optional[Tuple[type, Optional[UiAnno]]]:
        if args:
            field_type = args[0]
            for arg in args:
                if isinstance(arg, UiAnno):
                    return field_type, arg
            return field_type, None
        return None, None

    def render_element(
        self,
        ele: Element,
        key: str,
        classes: Optional[str] = None,
        field_arg: Optional[str] = None,
        **kwargs,
    ) -> None:
        kwargs = {**{"name": key}, **kwargs}
        placeholder = "placeholder"
        kwargs[placeholder] = __display_name__(kwargs[placeholder])
        compact = self.compact
        with Element().classes("flex flex-nowrap w-full"):
            ele_args = [item[0] for item in inspect.signature(ele.__init__).parameters.items()]
            compact = self.extend_kwargs(kwargs, ele_args, key, field_arg, ele)

            label: Optional[Label] = None
            if ele is not HiddenInput:
                label = Label(kwargs[placeholder])

                if compact and inspect.signature(ele).parameters.get(placeholder):
                    label.render_html = False
                else:
                    label.classes(self.label_classes)
                    label.render_html = True
            if not inspect.signature(ele).parameters.get(placeholder):
                kwargs.pop(placeholder)

            if self.instance and "placeholder" in ele_args:
                kwargs["placeholder"] = getattr(self.instance, key)
            el: Element = ele(**kwargs)
            if classes:
                el.classes(classes)
            if label:
                label.set_for(el)

    def extend_kwargs(self, kwargs: dict, ele_args: list[str], key: str, field_arg: str, ele: Element) -> bool:
        compact = self.compact
        if self.instance and "value" in ele_args:
            kwargs["value"] = getattr(self.instance, key)
            compact = False

        # radio button
        if self.instance and getattr(self.instance, key) == field_arg:
            kwargs["checked"] = "checked"
            compact = False
        elif self.instance and ele == Toggle:
            kwargs["checked"] = "checked"
            compact = False
        return compact

    def render_element_radio(
        self,
        ele: UiAnno,
        key: str,
        field_args: Tuple,
    ) -> None:
        Divider()
        for arg in field_args:
            self.render_element(Radio, key, ele.classes, placeholder=arg, field_arg=arg)
        Divider()

    def render_element_dropdown(self, field_class: type, key: str, placeholder: Optional[str]) -> None:
        if isinstance(placeholder, PydanticUndefinedType):
            placeholder = __display_name__(key)

        self.render_element(Dropdown, key, placeholder=placeholder, items=get_args(field_class))
