from playwright.sync_api import Locator

from playwright_tests.pages.widgets.widgets_page import WidgetsPage


class AccordionPage(WidgetsPage):
    # The site spells it "accordian" in the address too.
    PATH = "/accordian"

    SECTIONS = [
        "What is Lorem Ipsum?",
        "Where does it come from?",
        "Why do we use it?",
    ]

    @property
    def section_buttons(self) -> Locator:
        return self.page.locator(".accordion").get_by_role("button")

    def section_button(self, section: str) -> Locator:
        return self.page.get_by_role("button", name=section, exact=True)

    def section_body(self, section: str) -> Locator:
        item = self.page.locator(".accordion-item").filter(
            has=self.section_button(section)
        )
        return item.locator(".accordion-body")

    def toggle(self, section: str) -> None:
        self.section_button(section).click()

    def press_key_on(self, section: str, key: str) -> None:
        self.section_button(section).press(key)
