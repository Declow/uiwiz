from typing import Optional
from uiwiz.element import Element


class Tabs(Element):
    root_class: str = "tabs "
    _classes: str = "tabs-bordered"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Tabs.root_class + Tabs._classes)
        self.attributes["role"] = "tablist"

    def __exit__(self, *_):
        super().__exit__(*_)
        has_active = False
        first_child_tab = None
        for child in self.children:
            if not isinstance(child, Tab):
                continue

            if first_child_tab is None:
                first_child_tab = child

            if "checked" in child.attributes:
                has_active = True
        if not has_active:
            first_child_tab.active()


class Tab(Element):
    _classes: str = "tab"

    def __init__(self, title: str, active: Optional[bool] = None) -> None:
        self.selector = Element("input")
        self.selector.attributes["name"] = self.selector.parent_element.id
        self.selector.attributes["type"] = "radio"
        self.selector.attributes["aria-label"] = title
        self.selector.classes(self._classes)
        if active:
            self.active()

        super().__init__()
        self.classes("tab-content bg-base-100 border-base-300 p-4")
        self.attributes["role"] = "tabpanel"

    def active(self) -> "Tab":
        self.selector.attributes["checked"] = ""
        return self
