from typing import NamedTuple

from playwright.sync_api import Dialog, Locator

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage


class PopUp(NamedTuple):
    """What a browser pop-up showed: alert, confirm or prompt."""

    kind: str
    message: str


class AlertsPage(AlertsWindowsPage):
    PATH = "/alerts"

    # Every button is labelled "Click me", so each is found through the
    # sentence in its row.
    DESCRIPTIONS = {
        "alert": "Click Button to see alert",
        "timer": "On button click, alert will appear after 5 seconds",
        "confirm": "On button click, confirm box will appear",
        "prompt": "On button click, prompt box will appear",
    }

    @property
    def rows(self) -> Locator:
        return self.page.locator("#javascriptAlertsWrapper .row")

    def button(self, row: str) -> Locator:
        return self.rows.filter(has_text=self.DESCRIPTIONS[row]).get_by_role(
            "button", name="Click me", exact=True
        )

    @property
    def confirm_result(self) -> Locator:
        return self.page.locator("#confirmResult")

    @property
    def prompt_result(self) -> Locator:
        return self.page.locator("#promptResult")

    def click_and_answer(
        self, row: str, accept: bool = True, text: str | None = None
    ) -> PopUp:
        """Click a row's button, answer the pop-up and say what it showed.

        accept clicks OK, otherwise Cancel. text is typed into a prompt.
        Waits up to the page's default 30 seconds for the pop-up.
        """
        shown = []

        def answer(dialog: Dialog) -> None:
            shown.append(PopUp(dialog.type, dialog.message))
            if not accept:
                dialog.dismiss()
            elif text is None:
                dialog.accept()
            else:
                dialog.accept(text)

        # A pop-up freezes the page, and click() waits for the page, so the
        # pop-up must be answered by a handler set up before the click.
        self.page.once("dialog", answer)
        with self.page.expect_event("dialog"):
            self.button(row).click()
        return shown[0]
