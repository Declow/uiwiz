from pathlib import Path
from typing import Any, Optional, Tuple
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd
import json
from uiwiz.element import Element
from enum import Enum
import html

JS_PATH = Path(__file__).parent / "aggrid.js"


class Aggrid(Element):
    class OPTIONS(str, Enum):
        autoSizeColumn = "autoSizeAll"
        fitColumnContent = "sizeToFit"

    _classes: str = "ag-theme-alpine"

    def __init__(self, df: pd.DataFrame, column_option: OPTIONS = OPTIONS.autoSizeColumn) -> None:
        super().__init__("div", libraries=["/static/libs/aggrid-community.min.js"], extension=JS_PATH)
        self.classes(Aggrid._classes)

        cols, rows = Aggrid.create_cols_and_rows(df)

        self.attributes["style"] = "width: 100%;"

        self.attributes["hx-ext"] = "hx-aggrid"
        self.attributes["hx-aggrid-cols"] = cols
        self.attributes["hx-aggrid-rows"] = rows
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
