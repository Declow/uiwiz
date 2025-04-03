from uiwiz.element import Element


class Footer(Element):
    root_class: str = "mt-auto "
    _classes: str = "items-center p-4 bg-neutral text-neutral-content"

    def __init__(self) -> None:
        """Footer

        A footer is a section at the bottom of a page that contains information about the page.

        .. code-block:: python
            from uiwiz import ui

            with ui.footer():
                ui.label("Footer content")
        """
        super().__init__(tag="footer")
        self.classes(Footer._classes)
