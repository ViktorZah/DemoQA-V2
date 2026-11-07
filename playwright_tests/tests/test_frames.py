import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage
from playwright_tests.pages.frames_page import FramesPage
from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression

FRAME_SIZES = {"frame1": (500, 350), "frame2": (100, 100)}


@pytest.fixture
def frames_page(open_page):
    return open_page(FramesPage)


class TestFramesNavigation:
    @pytest.mark.smoke
    def test_frames_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_alerts_frame_and_windows()
        expect(page).to_have_url("https://demoqa.com/alertsWindows")

        section_page = AlertsWindowsPage(page)
        section_page.go_to_frames()
        expect(page).to_have_url("https://demoqa.com/frames")
        expect(section_page.heading).to_have_text("Frames")


class TestFramesContent:
    def test_intro_says_there_are_two_frames(self, frames_page):
        expect(frames_page.intro).to_be_visible()

    @pytest.mark.parametrize(
        "frame",
        [pytest.param("frame1", marks=pytest.mark.smoke), "frame2"],
    )
    def test_frame_shows_sample_page(self, frames_page, frame):
        expect(frames_page.frame_heading(frame)).to_have_text(
            "This is a sample page"
        )

    @pytest.mark.parametrize("frame", FramesPage.FRAMES)
    def test_frame_has_its_size(self, frames_page, frame):
        expect(frames_page.frame_box(frame)).to_be_visible()

        assert frames_page.frame_size(frame) == FRAME_SIZES[frame]

    def test_page_heading_is_separate_from_frames(self, frames_page):
        expect(frames_page.frame_heading("frame1")).to_be_visible()

        expect(frames_page.heading).to_have_text("Frames")


class TestFramesKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the intro misspells 'inspector' as 'inspecter'.",
    )
    def test_intro_spells_inspector_correctly(self, frames_page):
        expect(frames_page.intro).to_be_visible()

        assert "inspecter" not in frames_page.intro.inner_text()

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the intro runs 'Sample Iframe page' into the next "
            "sentence with no full stop."
        ),
    )
    def test_intro_sentences_are_separated(self, frames_page):
        expect(frames_page.intro).to_be_visible()

        assert "Sample Iframe page There" not in frames_page.intro.inner_text()
