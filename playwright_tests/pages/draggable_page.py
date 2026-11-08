from playwright.sync_api import Locator

from playwright_tests.pages.interactions_page import InteractionsPage


class DraggablePage(InteractionsPage):
    """Four tabs of drag examples. The site spells the page "Dragabble".

    The boxes have no roles or names, so they are found by ID or class.
    """

    PATH = "/dragabble"

    def tab(self, name: str) -> Locator:
        return self.page.get_by_role("tab", name=name, exact=True)

    def show(self, name: str) -> None:
        self.tab(name).click()

    @property
    def body(self) -> Locator:
        """The page body, whose mouse cursor changes during some drags."""
        return self.page.locator("body")

    def box(self, name: str) -> Locator:
        """A draggable box, by a short name."""
        boxes = {
            "simple": "#dragBox",
            "only x": "#restrictedX",
            "only y": "#restrictedY",
            "in container": "#containmentWrapper .draggable",
            "in parent": (
                "#draggableExample-tabpane-containerRestriction"
                " > .draggable .ui-widget-header"
            ),
            "cursor centre": "#cursorCenter",
            "cursor top left": "#cursorTopLeft",
            "cursor bottom": "#cursorBottom",
        }
        return self.page.locator(boxes[name])

    @property
    def container(self) -> Locator:
        return self.page.locator("#containmentWrapper")
