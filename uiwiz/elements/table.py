from typing import Callable, List, Optional, get_type_hints

import numpy as np
import pandas as pd
from pydantic import BaseModel

from uiwiz.element import Element
from uiwiz.element_types import ELEMENT_SIZE
from uiwiz.elements.button import Button
from uiwiz.elements.form import Form
from uiwiz.model_handler import ModelForm


class Table(Element):
    _classes_container: str = "w-full overflow-x-auto uiwiz-container-border-radius"
    _classes_table: str = (
        "table table-zebra table-auto bg-base-300 overflow-scroll w-full whitespace-nowrap uiwiz-td-padding"
    )

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self.classes(Table._classes_container)
        df = df.replace({np.nan: "None"})

        with self:
            with Element("table").classes(Table._classes_table):
                # columns
                with Element("thead"):
                    with Element("tr"):
                        for col in df.columns:
                            Element("th", content=col)
                # rows
                with Element("tbody"):
                    for _, row in df.iterrows():
                        with Element("tr"):
                            for _, val in row.items():
                                Element("td", content=val)


class ModelFormRender(ModelForm):
    def render_model(self, *args, **kwargs) -> Form:
        self.button = Button("Save")
        self.button.render_html = False


class TableV2(Element):
    root_size: str = "table-{size}"
    _classes_container: str = "w-full overflow-x-auto uiwiz-container-border-radius"
    _classes_table: str = (
        "table table-zebra table-auto bg-base-300 overflow-scroll w-full whitespace-nowrap uiwiz-td-padding"
    )

    def __init__(self, data: List[BaseModel]) -> None:
        super().__init__()
        self.classes(Table._classes_container)
        if data is None or data == []:
            pass

        self.data = data
        self.schema = list(data[0].model_fields.keys())
        self.did_render: bool = False
        self.edit: Optional[Callable] = None
        self.id_column_name: Optional[str] = None

    def edit_row(self, edit: Callable, id_column_name: str) -> "TableV2":
        self.edit = edit
        self.id_column_name = id_column_name
        return self

    @classmethod
    def render_edit_row(
        cls,
        model: BaseModel,
        id_column_name: str,
        save: Callable,
        cancel: Callable,
        size: ELEMENT_SIZE = "sm",
        **kwargs,
    ):
        with Element("tr") as container:
            rendere = ModelFormRender(model, size=size)
            hints = get_type_hints(model, include_extras=True)
            for key, field_type in hints.items():
                with Element("td"):
                    rendere.render_model_attributes(key, field_type, **kwargs)

            TableV2.__render_save_button__(container, save, cancel, id_column_name, model, size)

    @classmethod
    def __render_save_button__(
        cls,
        container: Element,
        save: Callable,
        cancel: Callable,
        id_column_name: str,
        model: BaseModel,
        size: ELEMENT_SIZE = "sm",
    ) -> Element:
        with Element("td"):
            Button("Cancel").size(size).on(
                "click",
                cancel,
                container,
                "outerHTML",
                params={id_column_name: model.__getattribute__(id_column_name)},
            ).attributes["hx-include"] = "closest tr"
            Button("Save").size(size).on(
                "click",
                save,
                container,
                "outerHTML",
                params={id_column_name: model.__getattribute__(id_column_name)},
            ).attributes["hx-include"] = "closest tr"

    def before_render(self):
        super().before_render()
        if self.did_render:
            return None

        with self:
            with Element("table").classes(Table._classes_table):
                # columns
                with Element("thead"):
                    with Element("tr"):
                        for col in self.schema:
                            Element("th", content=col)
                        if self.edit:
                            Element("th")
                # rows
                with Element("tbody"):
                    for row in self.data:
                        self.render_row(row, self.edit, self.id_column_name)

        self.did_render = True

    @classmethod
    def render_row(
        cls, row: BaseModel, edit: Optional[Callable], id_column_name: str, size: ELEMENT_SIZE = "sm"
    ) -> "TableV2":
        with Element("tr") as container:
            for item in list(row.model_fields.keys()):
                Element("td", content=row.__getattribute__(item))
            if edit:
                with Element("td"):
                    Button("Edit").size(size).on(
                        "click",
                        edit,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    )
        return container
