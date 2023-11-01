from uiwis.element import Element

class Footer(Element):
    def __init__(self) -> None:
        super().__init__(tag="footer")
        self._classes = "footer mt-auto p-8 bg-neutral text-neutral-content"