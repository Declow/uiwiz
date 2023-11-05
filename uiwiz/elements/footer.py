from uiwiz.element import Element

class Footer(Element):
    _classes: str = "mt-auto items-center p-4 bg-neutral text-neutral-content"

    def __init__(self) -> None:
        super().__init__(tag="footer")
        self.classes(Footer._classes)