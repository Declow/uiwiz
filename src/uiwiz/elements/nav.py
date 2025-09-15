from uiwiz.element import Element


class Nav(Element):
    root_class: str = "navbar w-full gap-4"
    root_size: str = "navbar-{size}"

    def __init__(self) -> None:
        """Nav
        
        This element is used for navigation bars

        .. code-block:: python
            from uiwiz import ui

            with ui.nav():
                ui.link("Home", "/")
                ui.link("Docs", "/docs")
        
        """
        super().__init__()
