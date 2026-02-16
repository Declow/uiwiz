from pathlib import Path

from docs.layout import Layout, Page
from docs.pages.docs.elements import create_docs_element, create_elements
from fastapi import Request

from uiwiz import PageRouter, ui

parent = Path(__file__).parent


class LayoutDocs(Layout):
    def after_render(self, request: Request) -> None:
        self.drawer.always_open(True)


docs_router = PageRouter(prefix="/reference")


@docs_router.page("/element/{name}", title="Elements")
async def docs_element(name: str) -> None:
    create_docs_element(getattr(ui, name), docs_router)


@docs_router.page("/elements", title="Elements")
async def docs_elements() -> None:
    create_elements(docs_router)


async def reference() -> None:
    with ui.container(padding="p-4"):
        ui.markdown("This is the reference page. It will contain links to all the elements and their documentation.")
        for value in dir(ui):
            if value.startswith("_"):
                continue
            ui.link(value, f"{docs_router.prefix}/element/{value}")
        ui.link("All Elements", f"{docs_router.prefix}/elements")


Page(path=f"{docs_router.prefix}/", title="Reference", file=reference)
