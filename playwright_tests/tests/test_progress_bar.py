import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.progress_bar_page import ProgressBarPage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

BLUE = "rgb(13, 202, 240)"
GREEN = "rgb(25, 135, 84)"


@pytest.fixture
def progress_bar_page(open_page):
    return open_page(ProgressBarPage)


def expect_progress(progress_bar_page, percent):
    """Check the bar's text, width and aria-valuenow agree."""
    bar = progress_bar_page.bar
    expect(bar).to_have_text(f"{percent}%")
    expect(bar).to_have_attribute("aria-valuenow", str(percent))
    expect(bar).to_have_attribute("style", f"width: {percent}%;")


def expect_ready_to_start(progress_bar_page):
    """Check the bar is empty and blue, with only Start offered."""
    expect_progress(progress_bar_page, 0)
    expect(progress_bar_page.bar).to_have_css("background-color", BLUE)
    expect(progress_bar_page.start_button).to_be_visible()
    expect(progress_bar_page.stop_button).to_have_count(0)
    expect(progress_bar_page.reset_button).to_have_count(0)


class TestProgressBarNavigation:
    @pytest.mark.smoke
    def test_progress_bar_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_progress_bar()
        expect(page).to_have_url("https://demoqa.com/progress-bar")
        expect(widgets_page.heading).to_have_text("Progress Bar")


class TestProgressBarInitialState:
    def test_bar_starts_empty_and_blue_with_start_button(
        self, progress_bar_page
    ):
        expect_ready_to_start(progress_bar_page)

    def test_bar_runs_from_0_to_100(self, progress_bar_page):
        expect(progress_bar_page.bar).to_have_attribute("aria-valuemin", "0")
        expect(progress_bar_page.bar).to_have_attribute(
            "aria-valuemax", "100"
        )


class TestProgressBarRunning:
    @pytest.mark.smoke
    def test_start_turns_into_stop(self, progress_bar_page):
        progress_bar_page.start()

        expect(progress_bar_page.stop_button).to_be_visible()
        expect(progress_bar_page.start_button).to_have_count(0)

    def test_bar_moves_forward_after_start(self, progress_bar_page):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(3_000)

        expect(progress_bar_page.bar).not_to_have_attribute(
            "aria-valuenow", "0"
        )

    def test_stop_holds_the_value(self, progress_bar_page):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(3_000)
        progress_bar_page.stop()
        expect(progress_bar_page.start_button).to_be_visible()
        stopped_at = progress_bar_page.value()

        progress_bar_page.let_time_pass(5_000)

        expect_progress(progress_bar_page, stopped_at)

    def test_start_after_stop_continues_from_stopped_value(
        self, progress_bar_page
    ):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(3_000)
        progress_bar_page.stop()
        stopped_at = progress_bar_page.value()

        progress_bar_page.start()
        progress_bar_page.let_time_pass(1_000)

        # Starting again from 0 would show about 10, less than stopped_at
        # (about 30), so a higher value proves the bar continued.
        assert progress_bar_page.value() > stopped_at


class TestProgressBarFinishing:
    @pytest.mark.smoke
    def test_bar_reaches_100_and_turns_green(self, progress_bar_page):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(ProgressBarPage.FULL_RUN_MS)

        expect_progress(progress_bar_page, 100)
        expect(progress_bar_page.bar).to_have_css("background-color", GREEN)

    def test_finished_bar_offers_only_reset(self, progress_bar_page):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(ProgressBarPage.FULL_RUN_MS)

        expect(progress_bar_page.reset_button).to_be_visible()
        expect(progress_bar_page.start_button).to_have_count(0)
        expect(progress_bar_page.stop_button).to_have_count(0)

    def test_reset_returns_bar_to_start(self, progress_bar_page):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(ProgressBarPage.FULL_RUN_MS)

        progress_bar_page.reset()

        expect_ready_to_start(progress_bar_page)

    def test_start_after_reset_runs_from_0_again(self, progress_bar_page):
        progress_bar_page.start()
        progress_bar_page.let_time_pass(ProgressBarPage.FULL_RUN_MS)
        progress_bar_page.reset()
        expect_progress(progress_bar_page, 0)

        progress_bar_page.start()
        progress_bar_page.let_time_pass(1_000)

        # About 10 after a second; well below 100 proves it began again.
        expect(progress_bar_page.stop_button).to_be_visible()
        assert 0 < progress_bar_page.value() < 50
