from re import Pattern

from playwright.sync_api import Locator

from playwright_tests.pages.base_page import BasePage


class SectionPage(BasePage):
    """A page with the sidebar menu and a main heading."""

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", level=1)

    def _menu_item(self, name: str | Pattern[str]) -> Locator:
        """Find a sidebar link by its exact name, or by a pattern."""
        return self.page.get_by_role("link", name=name, exact=True)
