import re

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage
from playwright_tests.pages.browser_windows_page import BrowserWindowsPage
from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.sample_page import MessageWindow, SamplePage

pytestmark = pytest.mark.regression

BROWSER_WINDOWS_URL = "https://demoqa.com/browser-windows"
SAMPLE_URL = "https://demoqa.com/sample"
MESSAGE = (
    "Knowledge increases by sharing but not by saving. Please share this "
    "website with your friends and in your organization."
)
# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000


@pytest.fixture
def browser_windows_page(open_page):
    return open_page(BrowserWindowsPage)


class TestBrowserWindowsNavigation:
    @pytest.mark.smoke
    def test_browser_windows_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_alerts_frame_and_windows()
        expect(page).to_have_url("https://demoqa.com/alertsWindows")

        section_page = AlertsWindowsPage(page)
        section_page.go_to_browser_windows()
        expect(page).to_have_url(BROWSER_WINDOWS_URL)
        expect(section_page.heading).to_have_text("Browser Windows")


class TestBrowserWindowsInitialState:
    def test_all_three_buttons_are_shown(self, browser_windows_page):
        expect(browser_windows_page.buttons).to_have_text(
            BrowserWindowsPage.BUTTONS
        )


class TestBrowserWindowsOpening:
    @pytest.mark.parametrize(
        "button",
        [pytest.param("New Tab", marks=pytest.mark.smoke), "New Window"],
    )
    def test_button_opens_sample_page(self, browser_windows_page, button):
        opened = SamplePage(browser_windows_page.open_with(button))

        expect(opened.page).to_have_url(SAMPLE_URL)
        expect(opened.heading).to_have_text("This is a sample page")

    def test_message_button_opens_window_with_message(
        self, browser_windows_page
    ):
        opened = MessageWindow(
            browser_windows_page.open_with("New Window Message")
        )

        expect(opened.text).to_have_text(MESSAGE)

    @pytest.mark.parametrize("button", BrowserWindowsPage.BUTTONS)
    def test_original_page_stays_open_and_unchanged(
        self, browser_windows_page, page: Page, button
    ):
        browser_windows_page.open_with(button)

        assert browser_windows_page.tab_count == 2
        expect(page).to_have_url(BROWSER_WINDOWS_URL)
        expect(browser_windows_page.button(button)).to_be_visible()


class TestBrowserWindowsKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the sample page has no title, so its tab shows only "
            "the address."
        ),
    )
    def test_sample_page_has_title(self, browser_windows_page):
        opened = browser_windows_page.open_with("New Tab")

        expect(opened).to_have_title(
            re.compile(r"\S"), timeout=QUICK_TIMEOUT_MS
        )
