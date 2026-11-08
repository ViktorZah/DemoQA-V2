from playwright.sync_api import Locator

from playwright_tests.pages.interactions_page import InteractionsPage


class SelectablePage(InteractionsPage):
    PATH = "/selectable"

    def tab(self, name: str) -> Locator:
        return self.page.get_by_role("tab", name=name, exact=True)

    def show(self, tab: str) -> None:
        self.tab(tab).click()

    # The items have no role and do not report being selected, so they are
    # found by their place in the page and their "active" class.
    @property
    def list_items(self) -> Locator:
        return self.page.locator("#verticalListContainer li")

    @property
    def grid_items(self) -> Locator:
        return self.page.locator("#gridContainer li")

    @property
    def selected_list_items(self) -> Locator:
        return self.page.locator("#verticalListContainer li.active")

    @property
    def selected_grid_items(self) -> Locator:
        return self.page.locator("#gridContainer li.active")

    def list_item(self, name: str) -> Locator:
        return self.list_items.filter(has_text=name)

    def grid_item(self, name: str) -> Locator:
        return self.grid_items.filter(has_text=name)

    def click_list_item(self, name: str) -> None:
        self.list_item(name).click()

    def click_grid_item(self, name: str) -> None:
        self.grid_item(name).click()

    def move_mouse_away(self) -> None:
        """Move the mouse onto the heading, so no item shows hover colour."""
        self.heading.hover()
