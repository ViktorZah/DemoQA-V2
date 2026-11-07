from playwright_tests.pages.section_page import SectionPage


class ElementsPage(SectionPage):
    PATH = "/elements"

    def go_to_broken_links(self) -> None:
        self._menu_item("Broken Links - Images").click()

    def go_to_upload_and_download(self) -> None:
        self._menu_item("Upload and Download").click()

    def go_to_dynamic_properties(self) -> None:
        self._menu_item("Dynamic Properties").click()
