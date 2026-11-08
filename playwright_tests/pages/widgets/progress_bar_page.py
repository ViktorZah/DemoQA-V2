from playwright.sync_api import Locator

from playwright_tests.pages.widgets.widgets_page import WidgetsPage


class ProgressBarPage(WidgetsPage):
    PATH = "/progress-bar"

    # A full run takes about 10.4 seconds of page time; this leaves room.
    FULL_RUN_MS = 15_000

    def open(self) -> None:
        """Open the page with Playwright's clock in control of its timers.

        The clock must be installed before the page loads. Time still flows
        normally, and let_time_pass() jumps it forward, so tests need no
        real 10-second waits.
        """
        self.page.clock.install()
        super().open()

    @property
    def bar(self) -> Locator:
        # The bar has no accessible name, so it is found by its role alone.
        return self.page.get_by_role("progressbar")

    def _button(self, name: str) -> Locator:
        return self.page.get_by_role("button", name=name, exact=True)

    @property
    def start_button(self) -> Locator:
        return self._button("Start")

    @property
    def stop_button(self) -> Locator:
        return self._button("Stop")

    @property
    def reset_button(self) -> Locator:
        return self._button("Reset")

    def start(self) -> None:
        self.start_button.click()

    def stop(self) -> None:
        self.stop_button.click()

    def reset(self) -> None:
        self.reset_button.click()

    def let_time_pass(self, ms: int) -> None:
        """Jump the page's clock forward, running its timers at once."""
        self.page.clock.run_for(ms)

    def value(self) -> int:
        return int(self.bar.get_attribute("aria-valuenow"))
