import pandas as pd
import json
from uiwiz.element import Element

class Aggrid(Element):
    _classes: str = "ag-theme-alpine"
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__("div", libraries=["/static/libs/aggrid.js"])
        self.classes(Aggrid._classes)

        self.attributes["style"] = "width: 100%;"

        cols = []
        rows = []
        if df is not None:
            cols = [{"field": item} for item in df.columns.to_list()]
            rows = json.dumps(df.to_dict("records"), default=str)

        self.script = f"""
        const columnDefs = {cols};
        const rowData = {rows};

        const gridOptions = {{
            columnDefs: columnDefs,
            rowData: rowData,
            domLayout: 'autoHeight'
        }};

        document.addEventListener('DOMContentLoaded', () => {{
            const gridDiv = document.querySelector('#{self.id}');
            new agGrid.Grid(gridDiv, gridOptions);
        }});

        """
