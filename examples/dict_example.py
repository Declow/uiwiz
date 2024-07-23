import uvicorn
from fastapi import Request

from uiwiz import UiwizApp, ui

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")


@app.page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes("col mx-auto"):
        json_data = {
            "name": "John Doe",
            "age": 30,
            "address": {"street": "123 Main St", "city": "Anytown", "country": "USA"},
            "hobbies": ["reading", "swimming", "coding"],
            "family": {"spouse": "Jane Doe", "children": [{"name": "Billy", "age": 5}, {"name": "Sally", "age": 3}]},
        }
        ui.json(json_data)


if __name__ == "__main__":
    uvicorn.run("dict_example:app", reload=True)
