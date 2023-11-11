import pandas as pd
from uiwiz.element import Element
import json

class ToastUIGrid(Element):
    def __init__(self, df: pd.DataFrame, id: str = None) -> None:
        super().__init__("div", libraries=["/static/libs/toastuigrid.js"])
        self.classes("toastgrid")
        cols = []
        rows = []
        if df is not None:
            cols = [{"header": item, "name": item} for item in df.columns.to_list()]
            rows = json.dumps(df.to_dict("records"), default=str)
        self.script = f"""
        var Grid = tui.Grid;
        var instance = new Grid({{
            columnOptions: {{
            minWidth: 180
        }},
            el: document.getElementById('{self.id if id is None else id}'),
            columns: {cols},
            data: {rows},
            usageStatistics: false
        }});

        Grid.applyTheme('striped');
        """