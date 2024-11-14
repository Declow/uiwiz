from typing import Callable, List, Optional, get_type_hints

import numpy as np
import pandas as pd
from pydantic import BaseModel

from uiwiz.element import Element
from uiwiz.element_types import ELEMENT_SIZE
from uiwiz.elements.button import Button
from uiwiz.elements.form import Form
from uiwiz.models.model_handler import ModelForm


class ModelFormRender(ModelForm):
    def render_model(self, *args, **kwargs) -> Form:
        self.button = Button("Save")
        self.button.render_html = False


class Table(Element):
    root_size: str = "table-{size}"
    _classes_container: str = "w-full overflow-x-auto uiwiz-container-border-radius"
    _classes_table: str = (
        "table table-zebra table-auto bg-base-300 overflow-scroll w-full whitespace-nowrap uiwiz-td-padding"
    )

    def __init__(self, data: List[BaseModel]) -> None:
        """
        Creates a table from a list of pydantic models

        :param data: A list of pydantic models

        :return: The current instance of the element.
        """
        super().__init__()
        self.classes(Table._classes_container)

        self.schema = []
        if data:
            self.schema = list(data[0].model_fields.keys())

        self.data = data
        self.did_render: bool = False
        self.edit: Optional[Callable] = None
        self.id_column_name: Optional[str] = None

    def edit_row(self, edit: Callable, id_column_name: str) -> "Table":
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

            Table.__render_save_button__(container, save, cancel, id_column_name, model, size)
        return container

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
        with Element("td").classes("flex justify-center join"):
            Button("Cancel").size(size).on(
                "click",
                cancel,
                container,
                "outerHTML",
                params={id_column_name: model.__getattribute__(id_column_name)},
            ).classes("btn-warning border border-base-content join-item flex-1").attributes["hx-include"] = "closest tr"
            Button("Save").size(size).on(
                "click",
                save,
                container,
                "outerHTML",
                params={id_column_name: model.__getattribute__(id_column_name)},
            ).classes("btn-success border border-base-content join-item flex-1").attributes["hx-include"] = "closest tr"

    def before_render(self) -> None:
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
    ) -> "Table":
        with Element("tr") as container:
            for item in list(row.model_fields.keys()):
                Element("td", content=row.__getattribute__(item))
            if edit:
                with Element("td").classes("flex justify-center"):
                    Button("Edit").classes("border border-base-content flex-1").size(size).on(
                        "click",
                        edit,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    )
        return container

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> Element:
        df = df.replace({np.nan: "None"})

        with Element().classes(Table._classes_container) as container:
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
        return container
