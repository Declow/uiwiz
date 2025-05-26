from contextlib import asynccontextmanager

import uvicorn
from fastapi import Request

from docs.layout import Layout, pages
from docs.page_docs import docs_router
from uiwiz import PageDefinition, PageRouter, UiwizApp, ui

router = PageRouter(page_definition_class=PageDefinition)
page_dict = {item.path: item for item in pages}

@asynccontextmanager
async def lifespan(app: UiwizApp):
    """Lifespan event handler for the application."""

    for page in pages:
        """
        Register each page with the application.
        This is the same as using the @app.page decorator,
        but allows for dynamic page registration.
        """
        app.page(path=page.path, title=page.title)(render_md)
        app.include_router(docs_router)

    yield


app = UiwizApp(theme="dim", lifespan=lifespan, page_definition_class=Layout)

def render_md(request: Request):
    page = page_dict.get(request.url.path, None)
    with open(f"docs/pages/{page.file_name}", "r") as f:
        content = f.read()

    with ui.container():
        ui.markdown(content)


if __name__ == "__main__":
    uvicorn.run("docs.main:app", host="0.0.0.0", port=8080, reload=True)
