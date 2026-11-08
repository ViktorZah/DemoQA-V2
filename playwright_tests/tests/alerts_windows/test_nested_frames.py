import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.alerts_windows.alerts_windows_page import (
    AlertsWindowsPage,
)
from playwright_tests.pages.alerts_windows.nested_frames_page import (
    NestedFramesPage,
)
from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression


@pytest.fixture
def nested_frames_page(open_page):
    return open_page(NestedFramesPage)


class TestNestedFramesNavigation:
    @pytest.mark.smoke
    def test_nested_frames_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_alerts_frame_and_windows()
        expect(page).to_have_url("https://demoqa.com/alertsWindows")

        section_page = AlertsWindowsPage(page)
        section_page.go_to_nested_frames()
        expect(page).to_have_url("https://demoqa.com/nestedframes")
        expect(section_page.heading).to_have_text("Nested Frames")


class TestNestedFramesContent:
    def test_intro_mentions_nested_frames(self, nested_frames_page):
        expect(nested_frames_page.intro).to_be_visible()

    @pytest.mark.smoke
    def test_parent_frame_shows_its_text(self, nested_frames_page):
        expect(nested_frames_page.parent_frame_text).to_have_text(
            "Parent frame"
        )

    def test_child_frame_shows_its_text(self, nested_frames_page):
        expect(nested_frames_page.child_frame_text).to_have_text(
            "Child Iframe"
        )

    def test_child_frame_is_inside_parent_frame(self, nested_frames_page):
        expect(nested_frames_page.frames_on_page).to_have_count(1)
        expect(nested_frames_page.frames_in_parent).to_have_count(1)

    def test_parent_frame_has_its_size(self, nested_frames_page):
        expect(nested_frames_page.parent_frame_box).to_be_visible()

        assert nested_frames_page.parent_frame_size() == (500, 350)


class TestNestedFramesKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the intro misspells 'inspector' as 'inspecter'.",
    )
    def test_intro_spells_inspector_correctly(self, nested_frames_page):
        expect(nested_frames_page.intro).to_be_visible()

        assert "inspecter" not in nested_frames_page.intro.inner_text()
