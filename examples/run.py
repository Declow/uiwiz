from datetime import date, datetime, timezone

from fastapi import Request
from pydantic import BaseModel

from data import df
from uiwiz import UiwizApp, ui, server
from uiwiz.element import Element as element

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


def e():
    ui.label("new label from htmx")


async def create_from_htmx(b: ui.button):
    with ui.label("This label came from htmx aka the server"):
        ui.label("Text from button " + b.content)


def create_label(message):
    ui.label(message)


async def update_res(request: Request, message: str):
    data = await request.json()
    create_label(f"{message} {data.get('input')}")


class DataInput(BaseModel):
    input: str


@app.ui("/test/path/param/{date}")
def run_with_path_param(date: date):
    with ui.element():
        ui.toast(date.isoformat())


@app.page("/")
async def test(request: Request):
    create_nav()
    with ui.container():
        with ui.row():
            ui.button("test").on_click(lambda: create_from_htmx(b))
            b = ui.button("asd").on_click(e)

            ui.button("Add toast").on_click(
                lambda: ui.toast("this is a toast very long toast"), swap="beforeend"
            ).classes("btn")

            ui.markdown("""This is **Markdown**.""")
        ui.markdown(
            """```python
if True:
    print("hi")
```"""
        )

        message = "New content:"

        def replace(request: Request, input: DataInput):
            create_label(f"{message} {input.input}")

        ui.input(
            name="input",
            placeholder="This is a placeholder",
        ).on("input", replace, lambda: res3.id, "outerHTML")
        with element() as res3:
            create_label(message)

        ui.textarea(
            name="input",
            placeholder="Placeholder",
        ).on("input, keyup[(ctrlKey||metaKey)&&keyCode==13]", replace, lambda: res2.id)
        res2 = ui.label(message)

        ui.table.from_dataframe(df)
        ui.aggrid(df)

        ui.button("Date").on_click(
            run_with_path_param, swap="none", params={"date": (datetime.now(tz=timezone.utc)).date().isoformat()}
        )

    with ui.footer():
        ui.label("some footer text")


if __name__ == "__main__":
    server.run("run:app")
