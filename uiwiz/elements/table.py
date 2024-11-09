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
        # self.save: Optional[Callable] = None

    def form(self, edit: Callable) -> "TableV2":
        self.edit = edit
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
                            Element("th", content=col)
                # rows
                self.__render_row__()

        self.did_render = True

    def __render_row__(self) -> "TableV2":
        with Element("tbody"):
            for row in self.data:
                with Element("tr") as container:
                    for item in list(row.model_fields.keys()):
                        Element("td", content=row.__getattribute__(item))
                    if self.edit:
                        Button("Edit").on("click", self.edit, container, "outerHTML")
        return self
