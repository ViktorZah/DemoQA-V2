import pytest

from selenium_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression


class TestHomePage:
    @pytest.mark.smoke
    def test_home_page_is_reached(self, driver):
        home_page = HomePage(driver)

        home_page.open()

        assert home_page.current_url == "https://demoqa.com/"
        assert home_page.title == "demosite"
        assert home_page.section_names() == [
            "Elements",
            "Forms",
            "Alerts, Frame & Windows",
            "Widgets",
            "Interactions",
            "Book Store Application",
        ]
