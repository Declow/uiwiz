from uiwis.element import Element

class Footer(Element):
    def __init__(self) -> None:
        super().__init__(tag="footer")
        self.classes("mt-auto items-center p-4 bg-neutral text-neutral-content")