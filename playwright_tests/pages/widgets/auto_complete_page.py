from playwright.sync_api import Locator

from playwright_tests.pages.widgets.widgets_page import WidgetsPage


class AutoCompletePage(WidgetsPage):
    """Two colour fields: one takes several colours, the other one."""

    PATH = "/auto-complete"

    # The fields are not tied to their labels, so they are found by ID.
    FIELDS = {
        "multiple": "#autoCompleteMultipleInput",
        "single": "#autoCompleteSingleInput",
    }

    def field(self, kind: str) -> Locator:
        return self.page.locator(self.FIELDS[kind])

    @property
    def suggestions(self) -> Locator:
        return self.page.get_by_role("option")

    @property
    def chosen_colours(self) -> Locator:
        """The colours chosen in the multiple field."""
        return self.page.locator(
            "#autoCompleteMultipleContainer .auto-complete__multi-value__label"
        )

    @property
    def single_colour(self) -> Locator:
        return self.page.locator(
            "#autoCompleteSingleContainer .auto-complete__single-value"
        )

    def type_into(self, kind: str, text: str) -> None:
        field = self.field(kind)
        field.click()
        field.fill(text)

    def choose(self, kind: str, colour: str) -> None:
        self.type_into(kind, colour)
        self.page.get_by_role("option", name=colour, exact=True).click()

    def press(self, kind: str, key: str) -> None:
        self.field(kind).press(key)

    def remove(self, colour: str) -> None:
        self.page.get_by_role("button", name=f"Remove {colour}").click()

    def clear_all(self) -> None:
        # The clear-all cross has no role or name.
        self.page.locator(
            "#autoCompleteMultipleContainer .auto-complete__clear-indicator"
        ).click()
