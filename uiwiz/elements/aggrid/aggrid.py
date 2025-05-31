import html
import json
from enum import Enum
from pathlib import Path
from typing import Any, Tuple

import numpy as np
import pandas as pd
from fastapi.responses import JSONResponse

from uiwiz.element import Element

LIB_PATH = Path(__file__).parent / "aggrid-community.min.js"
CSS_PATH = Path(__file__).parent / "aggridtheme.css"
JS_PATH = Path(__file__).parent / "aggrid.js"

class OPTIONS(str, Enum):
    autoSizeColumn = "autoSizeAll"
    fitColumnContent = "sizeToFit"

class Aggrid(Element, extensions=[CSS_PATH, LIB_PATH, JS_PATH]):


    _classes: str = "ag-theme-quartz ag-theme-uiwiz w-full"

    def __init__(self, df: pd.DataFrame) -> None:
        """Aggrid

        Use aggrid to display a DataFrame in a grid format.
        Can be used anywhere in a @page_router.ui("<path>") or @app.ui("<path>")

        Example:
        .. code-block:: python
        
            from uiwiz import ui
            import pandas as pd

            df = pd.DataFrame({
                "Name": ["Alice", "Bob", "Charlie"],
                "Age": [25, 30, 35],
                "City": ["New York", "Los Angeles", "Chicago"]
            })
            ui.aggrid(df) 

        :param df: The DataFrame to display in the grid
        """
        super().__init__("div")
        self.classes(Aggrid._classes)

        cols, rows = Aggrid.create_cols_and_rows(df)

        self.attributes["hx-ext"] = "hx-aggrid"
        self.attributes.__setitem__("hx-aggrid-cols", cols, False)
        self.attributes.__setitem__("hx-aggrid-rows", rows, False)
        self.attributes["hx-aggrid"] = "/data"

    @staticmethod
    def create_cols_and_rows(df: pd.DataFrame, escape: bool = True) -> Tuple[list[Any], list[Any]]:
        cols = []
        rows = []

        if df is not None:
            df = df.replace({np.nan: None})
            cols = [{"field": item} for item in df.columns.to_list()]
            rows = df.to_dict("records")
            if escape:
                cols = html.escape(json.dumps(cols))
                rows = html.escape(json.dumps(rows, default=str))

        return cols, rows

    @staticmethod
    def response(df: pd.DataFrame, headers: dict[str, str] = {}) -> JSONResponse:
        _headers = {"HX-Trigger": "aggridUpdate"} | headers
        cols, rows = Aggrid.create_cols_and_rows(df, False)
        return JSONResponse({"cols": cols, "rows": rows}, headers=_headers)
