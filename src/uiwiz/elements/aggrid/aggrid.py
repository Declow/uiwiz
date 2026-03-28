from __future__ import annotations

import html
import json
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fastapi.responses import JSONResponse

from uiwiz.element import Element

if TYPE_CHECKING:
    import polars as pl

LIB_PATH = Path(__file__).parent / "aggrid-community.min.js"
CSS_PATH = Path(__file__).parent / "aggridtheme.css"
JS_PATH = Path(__file__).parent / "aggrid.js"


class OPTIONS(str, Enum):
    autoSizeColumn = "autoSizeAll"
    fitColumnContent = "sizeToFit"


class Aggrid(Element, extensions=[CSS_PATH, LIB_PATH, JS_PATH]):
    _classes: str = "ag-theme-quartz ag-theme-uiwiz w-full"

    def __init__(self, df: pl.DataFrame | None) -> None:
        """Aggrid

        Use aggrid to display a DataFrame in a grid format.
        Can be used anywhere in a @page_router.ui("<path>") or @app.ui("<path>")

        Example:
        .. code-block:: python

            from uiwiz import ui
            import polars as pl

            df = pl.DataFrame({
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
    def create_cols_and_rows(
        df: pl.DataFrame | None,
        escape: bool = True,
    ) -> tuple[list[Any] | str, list[Any] | str]:
        cols = []
        rows = []

        if df is not None:
            cols = [{"field": item} for item in df.columns]
            rows = df.to_dicts()
            if escape:
                cols = html.escape(json.dumps(cols))
                rows = html.escape(json.dumps(rows, default=str))

        return cols, rows

    @staticmethod
    def response(df: pl.DataFrame | None, headers: dict[str, str] = {}) -> JSONResponse:
        _headers = {"HX-Trigger": "aggridUpdate"} | headers
        cols, rows = Aggrid.create_cols_and_rows(df, False)
        return JSONResponse({"cols": cols, "rows": rows}, headers=_headers)
