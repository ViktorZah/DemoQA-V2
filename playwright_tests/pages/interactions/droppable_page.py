import re

from playwright.sync_api import Locator

from playwright_tests.pages.interactions.interactions_page import (
    InteractionsPage,
)


class DroppablePage(InteractionsPage):
    """Four tabs of drag and drop examples.

    The boxes have no roles or names. Two drop boxes share the ID
    "droppable", so every part is found inside its tab's container.
    """

    PATH = "/droppable"

    # The tab is misspelled "Prevent Propogation"; either spelling is
    # accepted, so fixing it will not break the tests.
    TABS = {
        "Simple": "Simple",
        "Accept": "Accept",
        "Prevent Propagation": re.compile(r"^Prevent Prop[ao]gation$"),
        "Revert Draggable": "Revert Draggable",
    }
    # How far inside the greedy outer box to drop, to miss its inner box.
    OUTER_ONLY_OFFSET = (10, 10)

    def tab(self, name: str) -> Locator:
        return self.page.get_by_role(
            "tab", name=self.TABS[name], exact=True
        )

    def tab_named_exactly(self, name: str) -> Locator:
        return self.page.get_by_role("tab", name=name, exact=True)

    def show(self, name: str) -> None:
        self.tab(name).click()

    def _in(self, container: str, selector: str) -> Locator:
        return self.page.locator(f"#{container} {selector}")

    # Simple tab.
    @property
    def simple_box(self) -> Locator:
        return self._in("simpleDropContainer", "#draggable")

    @property
    def simple_target(self) -> Locator:
        return self._in("simpleDropContainer", "#droppable")

    # Accept tab.
    @property
    def acceptable_box(self) -> Locator:
        return self._in("acceptDropContainer", "#acceptable")

    @property
    def not_acceptable_box(self) -> Locator:
        return self.page.locator("#acceptDropContainer").get_by_text(
            "Not Acceptable", exact=True
        )

    @property
    def accept_target(self) -> Locator:
        return self._in("acceptDropContainer", ".drop-box")

    # Prevent Propagation tab.
    @property
    def propagation_box(self) -> Locator:
        return self._in("ppDropContainer", "#dragBox")

    def nested_box(self, name: str) -> Locator:
        """One of the four nested drop boxes, by a short name."""
        ids = {
            "not greedy outer": "#notGreedyDropBox",
            "not greedy inner": "#notGreedyInnerDropBox",
            "greedy outer": "#greedyDropBox",
            "greedy inner": "#greedyDropBoxInner",
        }
        return self._in("ppDropContainer", ids[name])

    def nested_box_text(self, name: str) -> Locator:
        # The first paragraph holds the box's own text, not its inner box's.
        return self.nested_box(name).locator(":scope > p")

    def drop_on_outer_only(self, name: str) -> None:
        self.drag_onto(
            self.propagation_box,
            self.nested_box(name),
            offset=self.OUTER_ONLY_OFFSET,
        )

    # Revert Draggable tab.
    @property
    def revert_box(self) -> Locator:
        return self._in("revertableDropContainer", "#revertable")

    @property
    def no_revert_box(self) -> Locator:
        return self._in("revertableDropContainer", "#notRevertable")

    @property
    def revert_target(self) -> Locator:
        return self._in("revertableDropContainer", "#droppable")

    @staticmethod
    def text_of(target: Locator) -> Locator:
        return target.locator(":scope > p")
