import re

from playwright_tests.pages.section_page import SectionPage


class WidgetsPage(SectionPage):
    PATH = "/widgets"

    def go_to_accordion(self) -> None:
        # The item is misspelled "Accordian"; either spelling is accepted,
        # so fixing it will not break navigation.
        self._menu_item(re.compile(r"^Accordi[ao]n$")).click()

    def go_to_auto_complete(self) -> None:
        self._menu_item("Auto Complete").click()

    def go_to_date_picker(self) -> None:
        self._menu_item("Date Picker").click()

    def go_to_slider(self) -> None:
        self._menu_item("Slider").click()

    def go_to_progress_bar(self) -> None:
        self._menu_item("Progress Bar").click()

    def go_to_tabs(self) -> None:
        self._menu_item("Tabs").click()
