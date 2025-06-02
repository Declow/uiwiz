from docs.layout import Layout, Page, pages
from docs.pages.docs.elements import create_elements
from uiwiz import PageRouter, ui


class LayoutDocs(Layout):
    def after_render(self, request):
        self.drawer.always_open(True)

docs_router = PageRouter(prefix="/docs")

index = Page(path=f"{docs_router.prefix}/", title="Docs", file_name="index.md")

pages.append(index)

@docs_router.page(path="/", title="Docs")
async def docs_index():
    with open("docs/pages/docs/index.md", "r") as f:
        content = f.read()
    with ui.container():
        ui.markdown(content)


@docs_router.page("/elements", title="Elements")
async def docs_elements():
    create_elements(docs_router)