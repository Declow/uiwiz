from src import ui
from src.page_route import PageRouter

router = PageRouter()


@router.page("/second_page", title="Second Page")
async def second_page():
    with ui.element().classes("col lg:px-80"):
        with ui.element().classes("w-full"):
            ui.element(content="Page 2!")
            ui.link("Home", "/")
