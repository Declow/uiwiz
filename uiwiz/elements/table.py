from typing import Callable, List, Optional, get_type_hints

import numpy as np
import pandas as pd
from pydantic import BaseModel

from uiwiz.element import Element
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
    _classes_container: str = "w-full overflow-x-auto uiwiz-container-border-radius"
    _classes_table: str = (
        "table table-sm table-zebra table-auto bg-base-300 overflow-scroll w-full whitespace-nowrap uiwiz-td-padding"
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
        self.show_id: bool = True

    def edit_row_with_id(self, edit: Callable, id_column_name: str) -> "TableV2":
        self.edit = edit
        self.id_column_name = id_column_name
        return self

    def edit_row_without_id(self, edit: Callable, id_column_name: str) -> "TableV2":
        self.edit = edit
        self.id_column_name = id_column_name
        self.show_id = False
        return self

    @classmethod
    def render_edit_row(cls, model: BaseModel, id_column_name: str, save: Callable, cancel: Callable, **kwargs):
        with Element("tr") as container:
            rendere = ModelFormRender(model)
            hints = get_type_hints(model, include_extras=True)
            for key, field_type in hints.items():
                with Element("td"):
                    rendere.render_model_attributes(key, field_type, **kwargs)

            TableV2.__render_save_button__(container, save, cancel, id_column_name, model)

    @classmethod
    def __render_save_button__(
        cls, container: Element, save: Callable, cancel: Callable, id_column_name: str, model: BaseModel
    ) -> Element:
        with Element("td"):
            Button("Cancel").classes("btn-sm").on(
                "click",
                cancel,
                container,
                "none",
                params={id_column_name: model.__getattribute__(id_column_name)},
            )
            Button("Save").classes("btn-sm").on(
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
                            if self.show_id and self.id_column_name == col:
                                Element("th", content=col)
                            elif self.id_column_name != col:
                                Element("th", content=col)
                        if self.edit:
                            Element("th")
                # rows
                with Element("tbody"):
                    for row in self.data:
                        self.render_row(row, self.edit, self.id_column_name)

        self.did_render = True

    @classmethod
    def render_row(cls, row: BaseModel, edit: Optional[Callable], id_column_name: str) -> "TableV2":
        with Element("tr") as container:
            for item in list(row.model_fields.keys()):
                Element("td", content=row.__getattribute__(item))
            if edit:
                with Element("td"):
                    Button("Edit").classes("btn-sm").on(
                        "click",
                        edit,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    )
        return container
