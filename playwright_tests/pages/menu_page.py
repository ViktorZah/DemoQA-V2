from playwright.sync_api import Locator

from playwright_tests.pages.widgets_page import WidgetsPage


class MenuPage(WidgetsPage):
    PATH = "/menu"

    def open(self) -> None:
        """Open the page and wait until the content has stopped moving.

        Hover tests need a still page; see wait_for_header_to_settle.
        """
        super().open()
        self.wait_for_header_to_settle()

    # The menu is plain nested lists of links, with no menu roles to find
    # its levels by, so the levels are found by CSS.
    @property
    def main_items(self) -> Locator:
        return self.page.locator("#nav > li > a")

    @property
    def sub_items(self) -> Locator:
        return self.page.locator("#nav > li > ul > li > a")

    @property
    def sub_sub_items(self) -> Locator:
        return self.page.locator("#nav ul ul a")

    @staticmethod
    def shown(items: Locator) -> Locator:
        """Only the items now on show; hidden ones stay in the page."""
        return items.filter(visible=True)

    def _item(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    def hover_main_item(self, name: str) -> None:
        self._item(name).hover()

    def open_sub_sub_list(self) -> None:
        self.hover_main_item("Main Item 2")
        self._item("SUB SUB LIST »").hover()

    def move_mouse_away(self) -> None:
        """Move the mouse onto the page heading, away from the menu."""
        self.heading.hover()

    def sub_item_names(self) -> list[str]:
        return self.sub_items.all_text_contents()
