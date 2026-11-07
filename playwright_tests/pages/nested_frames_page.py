from playwright.sync_api import FrameLocator, Locator

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage


class NestedFramesPage(AlertsWindowsPage):
    """A page holding a parent frame, which holds a child frame."""

    PATH = "/nestedframes"

    @property
    def intro(self) -> Locator:
        return self.page.get_by_text("There are nested iframes in this page")

    @property
    def frames_on_page(self) -> Locator:
        return self.page.locator("iframe")

    @property
    def parent_frame_box(self) -> Locator:
        # The frames have no title, so no accessible name to find them by.
        return self.page.locator("#frame1")

    @property
    def _parent_frame(self) -> FrameLocator:
        return self.page.frame_locator("#frame1")

    @property
    def parent_frame_text(self) -> Locator:
        return self._parent_frame.locator("body")

    @property
    def frames_in_parent(self) -> Locator:
        return self._parent_frame.locator("iframe")

    @property
    def child_frame_text(self) -> Locator:
        # The child frame has no ID either, and is the parent's only frame.
        return self._parent_frame.frame_locator("iframe").locator("body")

    def parent_frame_size(self) -> tuple[float, float]:
        return self.size_of(self.parent_frame_box)
