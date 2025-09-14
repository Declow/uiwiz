from bs4 import BeautifulSoup
from pydantic import BaseModel

from src import ui


class TableData(BaseModel):
    input: str


def test_table():
    output = str(ui.table([TableData(input="data")]))
    soup = BeautifulSoup(output, "html.parser")

    # headers
    assert "input" == soup.select("th")[0].contents[0]
    # row
    assert "data" == soup.select("td")[0].contents[0]


def test_table_button(setup_app):
    endpoint = "/edit"

    @setup_app.ui(endpoint)
    def edit_func():
        pass

    output = str(ui.table([TableData(input="data")], "input").edit_row(edit_func))
    soup = BeautifulSoup(output, "html.parser")

    assert ["btn", "border", "border-base-content", "flex-1", "flex-initial", "btn-sm"] == soup.select("button")[
        0
    ].attrs["class"]
    assert "click" == soup.select("button")[0].attrs["hx-trigger"]
    assert endpoint == soup.select("button")[0].attrs["hx-post"]
    assert "outerHTML" == soup.select("button")[0].attrs["hx-swap"]


def test_table_edit_row(setup_app):
    edit_endpoint = "/edit"
    render_endpoint = "/render"

    @setup_app.ui(edit_endpoint)
    def edit_func():
        pass

    @setup_app.ui(render_endpoint)
    def render_row_func():
        pass

    output = str(ui.table.render_edit_row(TableData(input="data"), "input", render_row_func, edit_func))
    soup = BeautifulSoup(output, "html.parser")

    assert [
        "btn",
        "btn-warning",
        "border",
        "border-base-content",
        "join-item",
        "flex-1",
        "flex-initial",
        "btn-sm",
    ] == soup.select("button")[0].attrs["class"]

    # button edit
    assert "click" == soup.select("button")[0].attrs["hx-trigger"]
    assert edit_endpoint == soup.select("button")[0].attrs["hx-post"]
    assert "outerHTML" == soup.select("button")[0].attrs["hx-swap"]
    assert "Cancel" == soup.select("button")[0].contents[0]

    # button save
    assert "click" == soup.select("button")[1].attrs["hx-trigger"]
    assert render_endpoint == soup.select("button")[1].attrs["hx-post"]
    assert "outerHTML" == soup.select("button")[1].attrs["hx-swap"]
    assert "Save" == soup.select("button")[1].contents[0]
