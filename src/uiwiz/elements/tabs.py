from typing import Optional

from uiwiz.element import Element


class Tabs(Element):
    root_class: str = "tabs "
    _classes: str = "tabs-box"

    def __init__(self) -> None:
        """Tabs
        This element is used for tab navigation.
        It should be used as a context manager to create tabs.

        .. code-block:: python
            from uiwiz import ui

            with ui.tabs():
                with ui.tab("Tab 1").active():
                    ui.label("Content of Tab 1")
                with ui.tab("Tab 2"):
                    ui.label("Content of Tab 2")
                with ui.tab("Tab 3"):
                    ui.label("Content of Tab 3")

        """
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
        """Tab

        This element is used for tab navigation
        and should be used inside a :class:`Tabs` element.
        The first tab will be active by default if no active tab is set.

        .. code-block:: python
            from uiwiz import ui

            with ui.tabs():
                with ui.tab("Tab 1").active():
                    ui.label("Content of Tab 1")
                with ui.tab("Tab 2"):
                    ui.label("Content of Tab 2")
                with ui.tab("Tab 3"):
                    ui.label("Content of Tab 3")

        :param title: The title of the tab
        :param active: If the tab should be active by default. Defaults to None, which will make the first tab active.
        """
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
