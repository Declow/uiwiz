from docs.layout import Layout, Page, pages
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
    