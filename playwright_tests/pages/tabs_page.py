from playwright.sync_api import Locator

from playwright_tests.pages.widgets_page import WidgetsPage


class TabsPage(WidgetsPage):
    PATH = "/tabs"

    @property
    def tabs(self) -> Locator:
        return self.page.get_by_role("tab")

    def tab(self, name: str) -> Locator:
        return self.page.get_by_role("tab", name=name, exact=True)

    @property
    def shown_panels(self) -> Locator:
        # Role locators skip hidden elements, so this finds only the panel
        # on show.
        return self.page.get_by_role("tabpanel")

    def panel(self, name: str) -> Locator:
        """The panel named by its tab, through aria-labelledby."""
        return self.page.get_by_role("tabpanel", name=name, exact=True)

    def select(self, name: str) -> None:
        self.tab(name).click()

    def press_on_tab(self, name: str, key: str) -> None:
        self.tab(name).press(key)
