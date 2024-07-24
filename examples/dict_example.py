import uvicorn

from uiwiz import UiwizApp, ui

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.button("this is from a method")
        ui.themeSelector()


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
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
