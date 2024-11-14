from typing import Annotated

import uvicorn
from fastapi import Request
from pydantic import BaseModel, Field

from uiwiz import UiwizApp, ui
from uiwiz.elements.table import Table
from uiwiz.models.model_handler import UiAnno


# Define data model
class TableData(BaseModel):
    id: Annotated[str, UiAnno(ui.hiddenInput)]  # Override default input method
    input: str = Field(min_length=3)
    title: str
    des: str


# Our data source for the application
DATA = {
    "1": TableData(id="1", input="This is input", title="Some title", des="Description"),
    "2": TableData(id="2", input="This is input", title="Some title", des="Description"),
    "3": TableData(id="3", input="This is input", title="Some title", des="Description"),
    "4": TableData(id="4", input="This is input", title="Some title", des="Description"),
}


app = UiwizApp()


@app.ui("/save/row/")
async def save_row(model: TableData):
    DATA[model.id] = model
    Table.render_row(DATA[model.id], edit_row, "id")


@app.ui("/display/row/{id}")
async def display_row(id: str):
    Table.render_row(DATA[id], edit_row, "id")


@app.ui("/edit/row/{id}")
async def edit_row(id: str):
    Table.render_edit_row(
        DATA[id],
        "id",
        save_row,
        display_row,
    )


@app.page("/")
async def test(request: Request):
    with ui.nav().classes("bg-base-200"):
        ui.element(content="")
        ui.themeSelector()

    with ui.col().classes("lg:px-80"):
        ui.markdown("You need to define a page, edit, save and display endpoints")

        Table(list(DATA.values())).edit_row(edit_row, "id")


if __name__ == "__main__":
    uvicorn.run("edit_row:app", reload=True)
