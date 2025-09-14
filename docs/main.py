from contextlib import asynccontextmanager

import uvicorn
from fastapi import Request
from fastapi.responses import HTMLResponse

from docs.layout import Layout, Page, pages
from docs.page_docs import docs_router
from src import PageDefinition, PageRouter, UiwizApp, ui
from src.frame import Frame

router: PageRouter = PageRouter(page_definition_class=PageDefinition)
page_dict: dict[str, Page] = {item.path: item for item in pages}


@asynccontextmanager
async def lifespan(app: UiwizApp):
    """Lifespan event handler for the application."""

    for page in pages:
        """
        Register each page with the application.
        This is the same as using the @app.page decorator,
        but allows for dynamic page registration.
        """
        if page.content is None:
            continue
        app.page(path=page.path, title=page.title)(render_md)
        app.include_router(docs_router)

    yield


app: UiwizApp = UiwizApp(lifespan=lifespan, page_definition_class=Layout)


async def render_md(request: Request):
    page = page_dict.get(request.url.path, None)
    if page:
        await page.render()
    else:
        with ui.container(padding="p-4"):
            ui.markdown("Page not found.")


async def not_found():
    with ui.container(padding="p-4"):
        ui.markdown("Page not found. Please check the URL or return to the home page.")
        for page in pages:
            ui.link(page.title, page.path)


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    await app.page_definition_class().render(not_found, request, title="Not Found")
    return HTMLResponse(
        content=Frame.get_stack().render(),
        status_code=404,
        media_type="text/html",
    )


if __name__ == "__main__":
    uvicorn.run("docs.main:app", host="0.0.0.0", port=8080, reload=True)
