import uvicorn
from pydantic import BaseModel

from uiwiz import UiwizApp, ui

app = UiwizApp()


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
    uvicorn.run("ace_editor:app", reload=True)
