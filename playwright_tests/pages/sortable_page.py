from playwright.sync_api import Locator

from playwright_tests.pages.interactions_page import InteractionsPage


class SortablePage(InteractionsPage):
    PATH = "/sortable"

    # How far inside the target's edge a list item is dropped.
    EDGE_PX = 3

    def tab(self, name: str) -> Locator:
        return self.page.get_by_role("tab", name=name, exact=True)

    def show(self, tab: str) -> None:
        self.tab(tab).click()

    # The items have no role or name, only their text, so they are found
    # by their class inside each tab's panel.
    @property
    def list_items(self) -> Locator:
        return self.page.locator("#demo-tabpane-list .list-group-item")

    @property
    def grid_items(self) -> Locator:
        return self.page.locator("#demo-tabpane-grid .list-group-item")

    def move_in_list(self, name: str, onto: str) -> None:
        """Drag a list item into the place of another one.

        An item only takes the other's place when dropped past its middle
        in the direction of travel, so it is dropped just inside the far
        edge: the bottom when moving down, the top when moving up.
        """
        names = self.list_items.all_inner_texts()
        target = self.list_items.filter(has_text=onto)
        box = target.bounding_box()
        moving_down = names.index(onto) > names.index(name)
        y = box["height"] - self.EDGE_PX if moving_down else self.EDGE_PX
        self.list_items.filter(has_text=name).drag_to(
            target, target_position={"x": box["width"] / 2, "y": y}
        )

    def move_in_grid(self, name: str, onto: str) -> None:
        """Drag a grid item onto the middle of another one."""
        self.grid_items.filter(has_text=name).drag_to(
            self.grid_items.filter(has_text=onto)
        )
