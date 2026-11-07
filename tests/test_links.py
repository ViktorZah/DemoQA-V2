import re

import pytest

from pages.elements_page import ElementsPage
from pages.home_page import HomePage
from pages.links_page import LinksPage

pytestmark = pytest.mark.regression

LINKS_URL = "https://demoqa.com/links"
HOME_URL = "https://demoqa.com/"
# Status code and status text each API link should report.
API_RESPONSES = {
    "Created": ("201", "Created"),
    "No Content": ("204", "No Content"),
    "Moved": ("301", "Moved Permanently"),
    "Bad Request": ("400", "Bad Request"),
    "Unauthorized": ("401", "Unauthorized"),
    "Forbidden": ("403", "Forbidden"),
    "Not Found": ("404", "Not Found"),
}


@pytest.fixture
def links_page(open_page):
    return open_page(LinksPage)


class TestLinksNavigation:
    @pytest.mark.smoke
    def test_links_is_reached_from_home_page(self, driver):
        home_page = HomePage(driver)
        home_page.open()

        home_page.go_to_elements()
        elements_page = ElementsPage(driver)
        assert elements_page.wait_for_url("https://demoqa.com/elements")

        elements_page.go_to_links()
        links_page = LinksPage(driver)
        assert links_page.wait_for_url(LINKS_URL)
        assert links_page.heading == "Links"


class TestLinksInitialState:
    def test_all_links_are_shown(self, links_page):
        labels = links_page.link_labels()

        # The second link's text is random, so it is checked on its own.
        assert labels[0] == "Home"
        assert labels[2:] == list(API_RESPONSES)
        assert len(labels) == 9

    def test_no_response_message_is_shown_at_first(self, links_page):
        assert links_page.response_message() is None


class TestLinksNewTab:
    @pytest.mark.parametrize(
        "link", [pytest.param("simple", marks=pytest.mark.smoke), "dynamic"]
    )
    def test_link_opens_home_page_in_new_tab(self, links_page, driver, link):
        links_page.click_new_tab_link(link)

        assert links_page.wait_for_tab_count(2)
        links_page.switch_to_newest_tab()
        home_page = HomePage(driver)
        assert home_page.wait_for_url(HOME_URL)
        assert "Elements" in home_page.section_names()

    @pytest.mark.parametrize("link", ["simple", "dynamic"])
    def test_original_tab_stays_on_links(self, links_page, link):
        links_page.click_new_tab_link(link)

        assert links_page.wait_for_tab_count(2)
        assert links_page.current_url == LINKS_URL

    def test_dynamic_link_text_is_home_and_five_characters(self, links_page):
        text = links_page.new_tab_link_text("dynamic")

        assert re.fullmatch(r"Home[A-Za-z0-9]{5}", text)

    def test_dynamic_link_text_changes_on_reload(self, links_page):
        first_text = links_page.new_tab_link_text("dynamic")

        links_page.reload()

        assert links_page.new_tab_link_text("dynamic") != first_text


class TestLinksApiCall:
    @pytest.mark.parametrize(
        "link",
        [
            pytest.param("Created", marks=pytest.mark.smoke),
            *list(API_RESPONSES)[1:],
        ],
    )
    def test_link_shows_its_status(self, links_page, link):
        status_code, status_text = API_RESPONSES[link]

        links_page.click_api_link(link)

        assert links_page.wait_for_response(status_code)
        assert links_page.response_values() == [status_code, status_text]

    def test_link_stays_on_page_in_same_tab(self, links_page):
        links_page.click_api_link("Created")
        assert links_page.wait_for_response("201")

        assert links_page.current_url == LINKS_URL
        assert links_page.tab_count == 1

    def test_next_link_replaces_previous_status(self, links_page):
        links_page.click_api_link("Created")
        assert links_page.wait_for_response("201")

        links_page.click_api_link("Forbidden")

        assert links_page.wait_for_response("403")
        assert links_page.response_values() == ["403", "Forbidden"]


class TestLinksKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: response message misspells 'status' as 'staus'.",
    )
    def test_response_message_is_spelled_correctly(self, links_page):
        links_page.click_api_link("Created")
        links_page.wait_for_response("201")

        assert links_page.response_message() == (
            "Link has responded with status 201 and status text Created"
        )
