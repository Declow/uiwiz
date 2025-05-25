import uvicorn

from docs.layout import Layout
from uiwiz import PageDefinition, PageRouter, UiwizApp, ui

app = UiwizApp(theme="dim", page_definition_class=Layout)

router = PageRouter(page_definition_class=PageDefinition)


@app.page("/")
def index():
    with ui.container():
        ui.label("Hello world").classes("text-3xl")
        ui.button("Click me")


@router.page(
    "/about",
)
def about():
    ui.label("About page").classes("text-3xl")
    ui.button("Click me")


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("docs.main:app", host="0.0.0.0", port=8080, reload=True)
