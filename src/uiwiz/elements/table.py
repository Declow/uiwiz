from typing import Callable, List, Optional, get_type_hints

import numpy as np
import pandas as pd
from pydantic import BaseModel

from uiwiz.element import Element
from uiwiz.element_types import ELEMENT_SIZE
from uiwiz.elements.button import Button
from uiwiz.elements.form import Form
from uiwiz.event import FUNC_TYPE
from uiwiz.models.model_handler import ModelForm


class ModelFormRender(ModelForm):
    def render_model(self, *args, **kwargs) -> Form:
        self.button = Button("Save")
        self.button.render_html = False


class Table(Element):
    root_size: str = "table-{size}"
    _classes_container: str = "w-full overflow-x-auto rounded-box "
    _classes_table: str = (
        "table table-zebra table-auto bg-base-300 overflow-scroll w-full whitespace-nowrap pr-4 pt-2 pb-2"
    )

    def __init__(self, data: List[BaseModel], id_column_name: Optional[str] = None) -> None:
        """
        Creates a table from a list of pydantic models

        Example:
        .. code-block:: python
            from uiwiz import ui
            from pydantic import BaseModel

            class User(BaseModel):
                id: int
                name: str
                email: str

            data = [
                User(id=1, name="John Doe", email="wiz@ui-wizard.com"),
                User(id=1, name="John Doe", email="wiz@ui-wizard.com"),
            ]
            ui.table(data, id_column_name="id")

        :param data: A list of pydantic models
        :param id_column_name: The name of the Pydantic attribute to be used with the path param endpoint. An endpoint like /path/{id} should have a attribute "id" on the class
        :return: The current instance of the element.
        """
        container = Element("div").classes("w-full")
        with container:
            super().__init__()
        self.classes(Table._classes_container)

        self.schema = []
        if data:
            self.schema = list(data[0].__class__.model_fields.keys())

        self.container = container
        self.data = data
        self.did_render: bool = False
        self.edit: Optional[FUNC_TYPE] = None
        self.delete: Optional[FUNC_TYPE] = None
        self.create: Optional[FUNC_TYPE] = None
        self.id_column_name: Optional[str] = id_column_name

    def set_border(self, border_classes: str = "border border-base-content") -> "Table":
        """
        Set the border classes for the table

        :param border_classes: The border classes to set
        :return: The current instance of the element.
        """
        self.classes(Table._classes_container + border_classes)
        return self

    def edit_row(self, edit: FUNC_TYPE) -> "Table":
        """
        Enable editing functionality for a table row.

        This method assigns the endpoint to handle the "Edit" action for rows
        in the table. It requires that `id_column_name` be set to identify rows uniquely.

        :param edit: The endpoint that is triggered when the "Edit" action is performed.
            The callback should accept parameters required to handle the editing logic.
        :type edit: FUNC_TYPE
        :return: Returns the `Table` instance with the "Edit" functionality enabled.
        :rtype: Table
        :raises ValueError: If `id_column_name` is not set, as it is required to identify rows
            for the "Edit" operation.

        Example:
            >>> table = Table(data, id_column_name="id").edit_row(edit=edit_endpoint)
        """
        if self.id_column_name is None:
            raise ValueError("When using edit id_column_name is required")
        self.edit = edit
        return self

    def delete_row(self, delete: FUNC_TYPE) -> "Table":
        """
        Enable deletion functionality for a table row.

        This method assigns the endpoint to handle the "Delete" action for rows
        in the table. It requires that `id_column_name` be set to identify rows uniquely.

        :param delete: The endpoint that is triggered when the "Delete" action is performed.
            The callback should accept parameters required to handle the deletion logic.
        :type delete: FUNC_TYPE
        :return: Returns the `Table` instance with the "Delete" functionality enabled.
        :rtype: Table
        :raises ValueError: If `id_column_name` is not set, as it is required to identify rows
            for the "Delete" operation.

        Example:
            >>> table = Table(data, id_column_name="id").delete_row(delete=delete_endpoint)
        """
        if self.id_column_name is None:
            raise ValueError("When using delete id_column_name is required")
        self.delete = delete
        return self

    def create_row(self, create: FUNC_TYPE) -> "Table":
        """
        Enable creation functionality for a table row.

        This method assigns the endpoint to handle the "Create" action for a row
        in the table.

        :param create: The endpoint that is triggered when the "Delete" action is performed.
        :type create: FUNC_TYPE
        :return: Returns the `Table` instance with the "Delete" functionality enabled.
        :rtype: Table

        Example:
            >>> table = Table(data).create_row(create=create_endpoint)
        """
        self.create = create
        return self

    @classmethod
    def render_edit_row(
        cls,
        model: BaseModel,
        id_column_name: str,
        save: FUNC_TYPE,
        cancel: FUNC_TYPE,
        size: ELEMENT_SIZE = "sm",
        **kwargs,
    ) -> Element:
        """
        Render a table row with inputs and cancel/save button

        :param model: The Pydantic model to render
        :param id_column_name: The column that should be used with edit or delete as path param
        :param save: The endpoint to call when save button is clicked
        :param cancel: The endpoint to call when cancel is clicked
        :param size: The size of the inputs
        :return: The tr element container
        """
        with Element("tr") as container:
            rendere = ModelFormRender(model, size=size)
            hints = get_type_hints(model, include_extras=True)
            for key, field_type in hints.items():
                with Element("td"):
                    rendere.render_model_attributes(key, field_type, **kwargs)

            Table.__render_save_button__(container, save, cancel, id_column_name, model, size, **kwargs)
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
        **kwargs,
    ) -> Element:
        with Element("td").classes("flex justify-end join"):
            Button("Cancel").size(size).on(
                "click",
                cancel,
                container,
                "outerHTML",
                params={
                    id_column_name: (
                        model.__getattribute__(id_column_name)
                        if isinstance(model, BaseModel)
                        else kwargs.get(id_column_name, {}).get("value")
                    )
                },
            ).classes("btn-warning border border-base-content join-item flex-1 flex-initial").attributes[
                "hx-include"
            ] = "closest tr"
            Button("Save").size(size).on(
                "click",
                save,
                container,
                "outerHTML",
                params={
                    id_column_name: (
                        model.__getattribute__(id_column_name)
                        if isinstance(model, BaseModel)
                        else kwargs.get(id_column_name, {}).get("value")
                    )
                },
            ).classes("btn-success border border-base-content join-item flex-1 flex-initial").attributes[
                "hx-include"
            ] = "closest tr"

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
                with Element("tbody") as container:
                    for row in self.data:
                        self.render_row(row, self.id_column_name, self.edit, self.delete)
        if self.create:
            with self.container:
                with Element().classes("pt-2 pb-2"):
                    Button("Add").on_click(self.create, container, swap="beforeend")
        self.did_render = True

    @classmethod
    def render_row(
        cls,
        row: BaseModel,
        id_column_name: Optional[str] = None,
        edit: Optional[FUNC_TYPE] = None,
        delete: Optional[FUNC_TYPE] = None,
        size: ELEMENT_SIZE = "sm",
    ) -> Element:
        """
        Render a table row

        :param row: The instance Pydantic model to render
        :param id_column_name: The optional column that should be used with edit or delete
        :param edit: The optional endpoint to call with the path param from id_column_name
        :param delete: The optional endpoint to call with the parh param from id_column_name
        :return: The tr element container
        """
        with Element("tr") as container:
            for item in list(row.__class__.model_fields.keys()):
                Element("td", content=row.__getattribute__(item))
            if edit and delete:
                with Element("td").classes("flex justify-end join"):
                    Button("Edit").classes("border border-base-content flex-1 join-item flex-initial").size(size).on(
                        "click",
                        edit,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    )
                    Button("Delete").classes("btn-error border border-base-content join-item flex-1 flex-initial").size(
                        size
                    ).on(
                        "click",
                        delete,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    ).attributes["hx-confirm"] = "Are you sure?"
            elif edit:
                with Element("td").classes("flex justify-end"):
                    Button("Edit").classes("border border-base-content flex-1 flex-initial").size(size).on(
                        "click",
                        edit,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    )
            elif delete:
                with Element("td").classes("flex justify-end"):
                    Button("Delete").classes("border border-base-content flex-1 flex-initial").size(size).on(
                        "click",
                        delete,
                        container,
                        "outerHTML",
                        params={id_column_name: row.__getattribute__(id_column_name)},
                    )
        return container

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> Element:
        """
        Render a pandas.DataFrame

        :param df: The DataFrame to render
        :return: The container element
        """
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
