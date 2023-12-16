from uiwiz.element import Element


class Footer(Element):
    root_class: str = "mt-auto "
    _classes: str = "items-center p-4 bg-neutral text-neutral-content"

    def __init__(self) -> None:
        super().__init__(tag="footer")
        self.classes(Footer._classes)
