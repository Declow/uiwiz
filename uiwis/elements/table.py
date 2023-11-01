from uiwis.element import Element
import pandas as pd

class Table(Element):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self.classes("overflow-x-auto")
        with self:
            with Element("table").classes("table table-zebra bg-base-300"):
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