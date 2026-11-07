import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression


class TestHomePage:
    @pytest.mark.smoke
    def test_home_page_is_reached(self, page: Page):
        home_page = HomePage(page)

        home_page.open()

        expect(page).to_have_url("https://demoqa.com/")
        expect(page).to_have_title("demosite")
        expect(home_page.section_titles).to_have_text(
            [
                "Elements",
                "Forms",
                "Alerts, Frame & Windows",
                "Widgets",
                "Interactions",
                "Book Store Application",
            ]
        )
