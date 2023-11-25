from uuid import uuid4

from fastapi import Request
from uiwiz.element import Element, Frame

class Tabs(Element):
    _classes: str = "tabs"

    def __init__(self) -> None:
        with Element() as container:
            super().__init__("div")
            self.classes(Tabs._classes)


class Tab(Element):
    _classes: str = "tab tab-bordered"
    _classes_active: str = " tab-active"

    def __init__(self, title: str) -> None:
        super().__init__("a")
        self.classes(Tab._classes)
        self.content = title
        container = self.parent_element.parent_element

        async def handle_tab(request: Request):
            data = await request.json()
            Tab.change_tab(container, data["active_tab"])

        self.event = {
            "func": handle_tab,
            "inputs": None,
            "trigger": "click",
            "endpoint": None,
            "target": f"#{container.id}",
            "swap": None,
            "vals": f'{{"active_tab": "{title}"}}',
        }

    
    def change_tab(container: Element, active_tab: str):
        frame = Frame.get_stack()
        container.set_frame(frame)
        frame.root_element = container

        tabs: TabPanels = Tab.get_tab_panel(container)
        tab: TabPanel
        for tab in tabs.children:
            if tab.tab.content == active_tab:
                tab.tab.classes(Tab._classes + Tab._classes_active)
                tabs.active_tab = tab.tab
                tab.render_html = True
            else:
                tab.tab.classes(Tab._classes)

    def get_tab_panel(container: Element):
        child: Element
        for child in container.children:
            if isinstance(child, TabPanels):
                return child
            

class TabPanels(Element):
    def __init__(self, tabs: Tabs, active_tab: Tab) -> None:
        super().__init__("div")
        active_tab.attributes["class"] = active_tab.attributes["class"] + Tab._classes_active
        self.tabs = tabs
        self.active_tab = active_tab

    def before_render(self):
        for child in self.children:
            child: TabPanel
            if child.tab != self.active_tab:
                child.render_html = False

    def __exit__(self, *_):
        self.stack.current_element = self.parent_element.parent_element

class TabPanel(Element):
    def __init__(self, tab: Tab) -> None:
        super().__init__("div")
        self.tab = tab
