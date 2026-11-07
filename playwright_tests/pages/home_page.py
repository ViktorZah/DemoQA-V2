from playwright.sync_api import Locator

from playwright_tests.pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    @property
    def section_titles(self) -> Locator:
        return self.page.locator(".category-cards").get_by_role("heading")

    def go_to_elements(self) -> None:
        self.page.get_by_role("link", name="Elements", exact=True).click()
