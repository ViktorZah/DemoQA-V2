from playwright_tests.pages.section_page import SectionPage


class InteractionsPage(SectionPage):
    # The section's own page has no heading.
    PATH = "/interaction"

    def open(self) -> None:
        """Open the page and wait until the content has stopped moving.

        Every Interactions page is about dragging or clicking positions,
        which need a still page; see wait_for_header_to_settle.
        """
        super().open()
        self.wait_for_header_to_settle()

    def go_to_sortable(self) -> None:
        self._menu_item("Sortable").click()

    def go_to_selectable(self) -> None:
        self._menu_item("Selectable").click()
