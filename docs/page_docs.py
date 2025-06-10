from pathlib import Path

from docs.layout import Layout, Page
from docs.pages.docs.elements import create_docs_element, create_elements
from uiwiz import PageRouter, ui

parent = Path(__file__).parent


class LayoutDocs(Layout):
    def after_render(self, request):
        self.drawer.always_open(True)


docs_router = PageRouter(prefix="/docs")


@docs_router.page("/element/{name}", title="Elements")
async def docs_element(name: str):
    create_docs_element(getattr(ui, name), docs_router)


@docs_router.page("/elements", title="Elements")
async def docs_elements():
    create_elements(docs_router)


async def docs_index():
    with ui.container():
        ui.markdown("This is the reference page. It will contain links to all the elements and their documentation.")
        for value in dir(ui):
            if value.startswith("_"):
                continue
            ui.link(value, f"{docs_router.prefix}/element/{value}")
        ui.link("All Elements", f"{docs_router.prefix}/elements")


Page(path=f"{docs_router.prefix}/", title="Docs", file=parent / "pages/docs/index.md")
Page(path=f"{docs_router.prefix}/reference", title="Reference", file=docs_index)
