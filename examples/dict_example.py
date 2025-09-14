import uvicorn

from src import UiwizApp, ui

app = UiwizApp()


def create_nav():
    with ui.nav():
        ui.themeSelector()


@app.page("/")
async def test():
    create_nav()
    with ui.element().classes("col lg:px-80"):
        json_data = {
            "name": "John Doe",
            "age": 50,
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "country": "USA",
                "more": {"obj": "nesting"},
            },
            "hobbies": ["reading", "swimming", "coding"],
            "family": {
                "spouse": "Jane Doe",
                "children": [
                    {
                        "name": "Billy",
                        "age": 20,
                        "children": [{"name": "test", "age": 1}],
                    },
                    {"name": "Sally", "age": 18},
                ],
            },
        }
        ui.dict(json_data, copy_to_clipboard=True)

        ui.dict([json_data, {"name": "Jane Doe", "age": 40}]).border_classes("")


if __name__ == "__main__":
    uvicorn.run("dict_example:app", reload=True)
