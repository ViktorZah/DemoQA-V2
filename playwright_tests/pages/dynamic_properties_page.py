from playwright.sync_api import Locator

from playwright_tests.pages.elements_page import ElementsPage


class DynamicPropertiesPage(ElementsPage):
    PATH = "/dynamic-properties"

    # The buttons change about 5 seconds after the page appears, which is
    # also Playwright's default limit, so checks for the change wait longer.
    CHANGE_TIMEOUT_MS = 10_000

    def _button(self, name: str) -> Locator:
        return self.page.get_by_role("button", name=name, exact=True)

    @property
    def enable_after_button(self) -> Locator:
        return self._button("Will enable 5 seconds")

    @property
    def color_change_button(self) -> Locator:
        return self._button("Color Change")

    @property
    def visible_after_button(self) -> Locator:
        return self._button("Visible After 5 Seconds")

    @property
    def random_id_text(self) -> Locator:
        # Its ID is new on every load, so it is found by its text.
        return self.page.get_by_text("This text has random Id", exact=True)
