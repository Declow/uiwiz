from contextlib import asynccontextmanager
import uvicorn
from pydantic import BaseModel

from uiwiz import UiwizApp, ui
from uiwiz.server import run



@asynccontextmanager
async def lifespan(app):
    print("")
    yield
    print("")

app = UiwizApp(lifespan=lifespan)

class DataInput(BaseModel):
    ace_data: str


@app.ui("/re")
def data(input: DataInput):
    print(input.ace_data)
    ui.toast(input.ace_data)


@app.page("/")
async def home_page():
    ui.label("Hello world")
    ui.themeSelector()

    with ui.form().on_submit(data):
        ui.ace(
            name="ace_data",
            lang="sql",
            content="SELECT * FROM table",
            sql_options={
                "tables": ["cars"],
                "columns": ["reg", "vin", "make", "model", "year"],
            },
        )
    ui.ace(name="ace_data", lang="sql", content="SELECT * FROM table")


if __name__ == "__main__":
    run("ace_editor:app")
