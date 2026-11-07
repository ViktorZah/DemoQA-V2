from playwright.sync_api import FrameLocator, Locator

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage


class FramesPage(AlertsWindowsPage):
    PATH = "/frames"

    FRAMES = ["frame1", "frame2"]

    @property
    def intro(self) -> Locator:
        return self.page.get_by_text("There are 2 Iframes in this page")

    def frame_box(self, frame: str) -> Locator:
        # The frames have no title, so no accessible name to find them by.
        return self.page.locator(f"#{frame}")

    def _frame(self, frame: str) -> FrameLocator:
        return self.page.frame_locator(f"#{frame}")

    def frame_heading(self, frame: str) -> Locator:
        return self._frame(frame).get_by_role("heading", level=1)

    def frame_size(self, frame: str) -> tuple[float, float]:
        return self.size_of(self.frame_box(frame))
