import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.elements.broken_links_page import BrokenLinksPage
from playwright_tests.pages.elements.elements_page import ElementsPage
from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression

HOME_URL = "https://demoqa.com/"
BROKEN_LINK_URL = "http://the-internet.herokuapp.com/status_codes/500"


@pytest.fixture
def broken_links_page(open_page):
    return open_page(BrokenLinksPage)


class TestBrokenLinksNavigation:
    @pytest.mark.smoke
    def test_broken_links_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_elements()
        expect(page).to_have_url("https://demoqa.com/elements")

        elements_page = ElementsPage(page)
        elements_page.go_to_broken_links()
        expect(page).to_have_url("https://demoqa.com/broken")
        expect(elements_page.heading).to_have_text("Broken Links - Images")


class TestBrokenLinksContent:
    def test_every_item_is_labelled(self, broken_links_page):
        expect(broken_links_page.labels).to_have_text(
            ["Valid image", "Broken image", "Valid Link", "Broken Link"]
        )

    def test_broken_image_does_not_load(self, broken_links_page):
        assert not broken_links_page.image_loaded("broken")


class TestBrokenLinksLinks:
    @pytest.mark.smoke
    def test_valid_link_opens_home_page_in_same_tab(
        self, broken_links_page, page: Page
    ):
        status = broken_links_page.follow_link("valid")

        assert status == 200
        expect(page).to_have_url(HOME_URL)
        assert broken_links_page.tab_count == 1

    def test_broken_link_opens_server_error_page_in_same_tab(
        self, broken_links_page, page: Page
    ):
        status = broken_links_page.follow_link("broken")

        assert status == 500
        expect(page).to_have_url(BROKEN_LINK_URL)
        assert broken_links_page.tab_count == 1


class TestBrokenLinksKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the valid image does not load. Its file is missing, "
            "and the server sends its HTML page instead."
        ),
    )
    def test_valid_image_loads(self, broken_links_page):
        assert broken_links_page.image_loaded("valid")

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: a missing file is answered with status 200 and the "
            "site's HTML page, not 404."
        ),
    )
    def test_missing_image_file_returns_not_found(self, broken_links_page):
        assert broken_links_page.image_file_status("broken") == 404
