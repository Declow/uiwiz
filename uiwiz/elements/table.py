from typing import Callable, List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel

from uiwiz.element import Element
from uiwiz.elements.button import Button


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


class TableV2(Element):
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
        self.show_id: bool = True
        # self.save: Optional[Callable] = None

    def edit_row_with_id(self, edit: Callable, id_column_name: str) -> "TableV2":
        self.edit = edit
        self.id_column_name = id_column_name
        return self

    def edit_row_without_id(self, edit: Callable, id_column_name: str) -> "TableV2":
        self.edit = edit
        self.id_column_name = id_column_name
        self.show_id = False
        return self

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
                        self.__render_row__(row)

        self.did_render = True

    def __render_row__(self, row: BaseModel) -> "TableV2":
        with Element("tr") as container:
            for item in list(row.model_fields.keys()):
                if self.show_id and self.id_column_name == item:
                    Element("td", content=row.__getattribute__(item))
                elif self.id_column_name != item:
                    Element("td", content=row.__getattribute__(item))
            if self.edit:
                with Element("td"):
                    Button("Edit").on(
                        "click",
                        self.edit,
                        container,
                        "outerHTML",
                        params={self.id_column_name: row.__getattribute__(self.id_column_name)},
                    )
        return self
