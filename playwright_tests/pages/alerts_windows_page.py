from playwright_tests.pages.section_page import SectionPage


class AlertsWindowsPage(SectionPage):
    """The Alerts, Frame & Windows section."""

    PATH = "/alertsWindows"

    def go_to_browser_windows(self) -> None:
        self._menu_item("Browser Windows").click()

    def go_to_alerts(self) -> None:
        self._menu_item("Alerts").click()

    def go_to_frames(self) -> None:
        self._menu_item("Frames").click()
