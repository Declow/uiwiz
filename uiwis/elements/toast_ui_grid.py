import pandas as pd
from uiwis.element import Element
import json

class ToastUIGrid(Element):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__("div")
        self.classes("col")
        cols = [{"header": item, "name": item} for item in df.columns.to_list()]
        rows = json.dumps(df.to_dict("records"), default=str)
        self.script = f"""
        const Grid = tui.Grid;
            const instance = new Grid({{
              columnOptions: {{
                minWidth: 180
            }},
            el: document.getElementById('{self.id}'),
            columns: {cols},
            data: {rows}
        }});

        Grid.applyTheme('striped');
        """