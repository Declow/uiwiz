from uiwiz.element import Element


class Avatar(Element):
    root_class: str = "avatar"
    _classes_inner: str = "w-{size} rounded-full"

    def __init__(self, path: str, size: int = 12) -> None:
        """
        Display an avatar image.

        :param path: The path to the image to display.
        :type path: str
        :param size: The size of the avatar.
        :type size: int, optional
        """
        super().__init__()
        with self:
            with Element("div").classes(Avatar._classes_inner.format(size=size)) as container:
                self.container = container
                img = Element("img")
                img.attributes["src"] = path

    def classes(self, input: str = ""):
        if hasattr(self, "container"):
            self.container.classes(input)
        return self
