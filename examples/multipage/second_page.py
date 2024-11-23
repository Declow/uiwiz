from uiwiz import ui
from uiwiz.page_route import PageRouterV2

router = PageRouterV2()


@router.page("/second_page", title="Second Page")
async def second_page():
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            ui.element(content="Page 2!")
            ui.link("Home", "/")
