import uvicorn

from uiwiz import UiwizApp, ui
from uiwiz.elements.dict import DictV2

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
        DictV2(json_data)

        DictV2([json_data])


if __name__ == "__main__":
    uvicorn.run("dict_example:app", reload=True)
