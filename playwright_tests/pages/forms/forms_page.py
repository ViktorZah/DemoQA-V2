from playwright_tests.pages.section_page import SectionPage


class FormsPage(SectionPage):
    PATH = "/forms"

    def go_to_practice_form(self) -> None:
        self._menu_item("Practice Form").click()
