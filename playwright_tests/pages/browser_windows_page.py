from playwright.sync_api import Locator, Page

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage


class BrowserWindowsPage(AlertsWindowsPage):
    PATH = "/browser-windows"

    BUTTONS = ["New Tab", "New Window", "New Window Message"]

    def button(self, name: str) -> Locator:
        return self.page.get_by_role("button", name=name, exact=True)

    @property
    def buttons(self) -> Locator:
        return self.page.locator("#browserWindows").get_by_role("button")

    def open_with(self, name: str) -> Page:
        """Click a button and return the tab or window it opens."""
        with self.page.context.expect_page() as new_page:
            self.button(name).click()
        opened = new_page.value
        opened.wait_for_load_state()
        return opened
