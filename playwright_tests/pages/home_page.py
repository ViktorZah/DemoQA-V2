from playwright.sync_api import Locator

from playwright_tests.pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    @property
    def section_titles(self) -> Locator:
        return self.page.locator(".category-cards").get_by_role("heading")

    def _section_card(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    def go_to_elements(self) -> None:
        self._section_card("Elements").click()

    def go_to_forms(self) -> None:
        self._section_card("Forms").click()
