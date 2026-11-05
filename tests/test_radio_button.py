import pytest

from pages.elements_page import ElementsPage
from pages.home_page import HomePage
from pages.radio_button_page import RadioButtonPage

pytestmark = pytest.mark.regression


@pytest.fixture
def radio_button_page(open_page):
    return open_page(RadioButtonPage)


class TestRadioButtonNavigation:
    @pytest.mark.smoke
    def test_radio_button_is_reached_from_home_page(self, driver):
        home_page = HomePage(driver)
        home_page.open()

        home_page.go_to_elements()
        elements_page = ElementsPage(driver)
        assert elements_page.wait_for_url("https://demoqa.com/elements")

        elements_page.go_to_radio_button()
        radio_button_page = RadioButtonPage(driver)
        assert radio_button_page.wait_for_url(
            "https://demoqa.com/radio-button"
        )
        assert radio_button_page.heading == "Radio Button"


class TestRadioButtonInitialState:
    def test_question_and_options_are_shown(self, radio_button_page):
        assert radio_button_page.question == "Do you like the site?"
        assert radio_button_page.option_labels() == [
            "Yes",
            "Impressive",
            "No",
        ]

    def test_nothing_is_selected_at_first(self, radio_button_page):
        assert radio_button_page.selected_options() == []
        assert radio_button_page.result() is None

    def test_yes_and_impressive_are_enabled(self, radio_button_page):
        assert radio_button_page.is_enabled("Yes")
        assert radio_button_page.is_enabled("Impressive")


class TestRadioButtonSelection:
    @pytest.mark.parametrize(
        "option",
        [
            pytest.param("Yes", marks=pytest.mark.smoke),
            "Impressive",
        ],
    )
    def test_selecting_an_option_shows_it_as_the_result(
        self, radio_button_page, option
    ):
        radio_button_page.select(option)

        assert radio_button_page.wait_for_result_to_be(option) == option
        assert radio_button_page.selected_options() == [option]
        message = radio_button_page.result_message
        assert message == f"You have selected {option}"

    def test_selecting_another_option_replaces_the_first(
        self, radio_button_page
    ):
        radio_button_page.select("Yes")
        assert radio_button_page.wait_for_result_to_be("Yes") == "Yes"

        radio_button_page.select("Impressive")

        shown = radio_button_page.wait_for_result_to_be("Impressive")
        assert shown == "Impressive"
        assert radio_button_page.selected_options() == ["Impressive"]

    def test_selecting_the_same_option_again_keeps_it(self, radio_button_page):
        radio_button_page.select("Yes")
        assert radio_button_page.wait_for_result_to_be("Yes") == "Yes"

        radio_button_page.select("Yes")

        assert radio_button_page.selected_options() == ["Yes"]
        assert radio_button_page.result() == "Yes"

    def test_refreshing_the_page_clears_the_selection(self, radio_button_page):
        radio_button_page.select("Yes")
        assert radio_button_page.wait_for_result_to_be("Yes") == "Yes"

        radio_button_page.driver.refresh()

        assert radio_button_page.selected_options() == []
        assert radio_button_page.result() is None


class TestRadioButtonKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the No option is disabled, so it cannot be chosen.",
    )
    def test_no_option_can_be_selected(self, radio_button_page):
        radio_button_page.select("No")

        assert radio_button_page.selected_options() == ["No"]
        assert radio_button_page.wait_for_result_to_be("No") == "No"

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the No option is disabled, so it cannot be chosen.",
    )
    def test_no_option_replaces_the_current_selection(self, radio_button_page):
        radio_button_page.select("Impressive")
        radio_button_page.wait_for_result_to_be("Impressive")

        radio_button_page.select("No")

        assert radio_button_page.selected_options() == ["No"]
        assert radio_button_page.wait_for_result_to_be("No") == "No"
