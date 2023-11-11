import pandas as pd
import json
from uiwiz.element import Element
from enum import Enum

class Aggrid(Element):
    class OPTIONS(str, Enum):
        autoSizeColumn = 'autoSizeAll'
        fitColumnContent = 'sizeToFit'

    _classes: str = "ag-theme-alpine"

    def __init__(self, df: pd.DataFrame, asd: str = None, column_option: OPTIONS = OPTIONS.autoSizeColumn) -> None:
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
            defaultColDef: {{
                resizable: true,
            }},
            columnDefs: columnDefs,
            rowData: rowData,
            domLayout: 'autoHeight',
            onFirstDataRendered: {column_option},
        }};

        function autoSizeAll(skipHeader) {{}}

        function sizeToFit() {{
            gridOptions.api.sizeColumnsToFit({{
                defaultMinWidth: 100
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const gridDiv = document.querySelector('#{self.id}');
            new agGrid.Grid(gridDiv, gridOptions);
        }});

        window.addEventListener('resize', () => {column_option}());
        """
