import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.interactions_page import InteractionsPage
from playwright_tests.pages.resizable_page import ResizablePage

pytestmark = pytest.mark.regression

START = (200, 200)
LIMITED_MIN = (150, 150)
LIMITED_MAX = (500, 300)


@pytest.fixture
def resizable_page(open_page):
    return open_page(ResizablePage)


class TestResizableNavigation:
    @pytest.mark.smoke
    def test_resizable_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_interactions()
        expect(page).to_have_url("https://demoqa.com/interaction")

        interactions_page = InteractionsPage(page)
        interactions_page.go_to_resizable()
        expect(page).to_have_url("https://demoqa.com/resizable")
        expect(interactions_page.heading).to_have_text("Resizable")


class TestLimitedBox:
    def test_states_its_size_and_limits(self, resizable_page):
        expect(resizable_page.box_text("limited")).to_have_text(
            "Resizable box, starting at 200x200. "
            "Min size is 150x150, max is 500x300."
        )

    def test_starts_at_200_by_200(self, resizable_page):
        assert resizable_page.box_size("limited") == START

    @pytest.mark.smoke
    def test_dragging_handle_resizes_it(self, resizable_page):
        resizable_page.resize("limited", 100, 50)

        assert resizable_page.box_size("limited") == (300, 250)

    def test_cannot_grow_past_its_maximum(self, resizable_page):
        resizable_page.resize("limited", 1000, 1000)

        assert resizable_page.box_size("limited") == LIMITED_MAX

    def test_cannot_shrink_past_its_minimum(self, resizable_page):
        resizable_page.resize("limited", -1000, -1000)

        assert resizable_page.box_size("limited") == LIMITED_MIN


class TestFreeBox:
    def test_starts_at_200_by_200(self, resizable_page):
        assert resizable_page.box_size("free") == START

    def test_dragging_handle_resizes_it(self, resizable_page):
        resizable_page.resize("free", 100, 50)

        assert resizable_page.box_size("free") == (300, 250)

    def test_can_grow_past_the_limited_maximum(self, resizable_page):
        resizable_page.resize("free", 600, 300)

        assert resizable_page.box_size("free") == (800, 500)

    def test_can_shrink_past_the_limited_minimum(self, resizable_page):
        resizable_page.resize("free", -1000, -1000)

        width, height = resizable_page.box_size("free")
        assert width < LIMITED_MIN[0] and height < LIMITED_MIN[1]
