from playwright.sync_api import Locator

from playwright_tests.pages.base_page import BasePage


class ElementsPage(BasePage):
    PATH = "/elements"

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", level=1)

    def _menu_item(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    def go_to_broken_links(self) -> None:
        self._menu_item("Broken Links - Images").click()

    def go_to_upload_and_download(self) -> None:
        self._menu_item("Upload and Download").click()
