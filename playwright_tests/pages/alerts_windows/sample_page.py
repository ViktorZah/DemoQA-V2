from playwright.sync_api import Locator

from playwright_tests.pages.base_page import BasePage


class SamplePage(BasePage):
    """The page that Browser Windows opens in a new tab or window."""

    PATH = "/sample"

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", level=1)


class MessageWindow(BasePage):
    """The blank window that only holds a written message."""

    PATH = "about:blank"

    @property
    def text(self) -> Locator:
        return self.page.locator("body")
