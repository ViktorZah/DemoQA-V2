from playwright.sync_api import Locator

from playwright_tests.pages.widgets_page import WidgetsPage


class ToolTipsPage(WidgetsPage):
    PATH = "/tool-tips"

    def open(self) -> None:
        """Open the page and wait until the content has stopped moving.

        Hover tests need a still page; see wait_for_header_to_settle.
        """
        super().open()
        self.wait_for_header_to_settle()

    @property
    def button(self) -> Locator:
        return self.page.get_by_role("button", name="Hover me to see")

    @property
    def text_field(self) -> Locator:
        # The field has no label, only a placeholder.
        return self.page.get_by_placeholder("Hover me to see")

    def _link(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True)

    def target(self, name: str) -> Locator:
        """A part of the page that has a tooltip, by a short name."""
        targets = {
            "button": self.button,
            "text field": self.text_field,
            "Contrary": self._link("Contrary"),
            "1.10.32": self._link("1.10.32"),
        }
        return targets[name]

    @property
    def tooltip(self) -> Locator:
        return self.page.get_by_role("tooltip")

    def tooltip_saying(self, text: str) -> Locator:
        return self.page.get_by_role("tooltip", name=text, exact=True)

    def hover(self, name: str) -> None:
        self.target(name).hover()

    def focus(self, name: str) -> None:
        self.target(name).focus()

    def move_mouse_away(self) -> None:
        """Move the mouse onto the page heading, which has no tooltip."""
        self.heading.hover()
