from uiwiz.element import Element
import pandas as pd


class Table(Element):
    root_class: str = "table "
    _classes_container: str = "overflow-x-auto"
    _classes_table: str = "table-zebra bg-base-300"

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self.classes(Table._classes_container)
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
