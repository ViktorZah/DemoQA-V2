import pytest
from selenium.webdriver.common.keys import Keys

from selenium_tests.pages.buttons_page import ButtonsPage
from selenium_tests.pages.elements_page import ElementsPage
from selenium_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression

CORRECT_CLICKS = {
    "Double Click Me": "double",
    "Right Click Me": "right",
    "Click Me": "left",
}
EXPECTED_MESSAGES = {
    "Double Click Me": "You have done a double click",
    "Right Click Me": "You have done a right click",
    "Click Me": "You have done a dynamic click",
}


@pytest.fixture
def buttons_page(open_page):
    return open_page(ButtonsPage)


class TestButtonsNavigation:
    @pytest.mark.smoke
    def test_buttons_is_reached_from_home_page(self, driver):
        home_page = HomePage(driver)
        home_page.open()

        home_page.go_to_elements()
        elements_page = ElementsPage(driver)
        assert elements_page.wait_for_url("https://demoqa.com/elements")

        elements_page.go_to_buttons()
        buttons_page = ButtonsPage(driver)
        assert buttons_page.wait_for_url("https://demoqa.com/buttons")
        assert buttons_page.heading == "Buttons"


class TestButtonsInitialState:
    def test_all_three_buttons_are_shown(self, buttons_page):
        assert buttons_page.button_labels() == [
            "Double Click Me",
            "Right Click Me",
            "Click Me",
        ]

    def test_no_message_is_shown_at_first(self, buttons_page):
        assert buttons_page.messages() == {}


class TestButtonsCorrectClick:
    @pytest.mark.parametrize(
        "button",
        [
            pytest.param("Double Click Me", marks=pytest.mark.smoke),
            "Right Click Me",
            "Click Me",
        ],
    )
    def test_correct_click_shows_only_that_message(
        self, buttons_page, button
    ):
        buttons_page.click_button(button, CORRECT_CLICKS[button])

        message = buttons_page.wait_for_message(button)
        assert message == EXPECTED_MESSAGES[button]
        assert buttons_page.messages() == {button: message}

    @pytest.mark.parametrize("button", CORRECT_CLICKS)
    def test_repeating_a_click_keeps_its_message(self, buttons_page, button):
        buttons_page.click_button(button, CORRECT_CLICKS[button])
        assert buttons_page.wait_for_message(button)

        buttons_page.click_button(button, CORRECT_CLICKS[button])

        assert buttons_page.messages() == {button: EXPECTED_MESSAGES[button]}

    def test_each_button_keeps_its_message_when_others_are_clicked(
        self, buttons_page
    ):
        for button, kind in CORRECT_CLICKS.items():
            buttons_page.click_button(button, kind)
            assert buttons_page.wait_for_message(button)

        assert buttons_page.messages() == EXPECTED_MESSAGES


class TestButtonsWrongClick:
    @pytest.mark.parametrize(
        ("button", "kind"),
        [
            ("Double Click Me", "left"),
            ("Double Click Me", "right"),
            ("Right Click Me", "left"),
            ("Right Click Me", "double"),
            ("Click Me", "right"),
        ],
    )
    def test_wrong_click_shows_no_message(self, buttons_page, button, kind):
        buttons_page.click_button(button, kind)

        # A correct click on another button proves the page has responded,
        # so the wrong click had time to show a message if it was going to.
        other = next(name for name in CORRECT_CLICKS if name != button)
        buttons_page.click_button(other, CORRECT_CLICKS[other])
        buttons_page.wait_for_message(other)

        assert buttons_page.messages() == {other: EXPECTED_MESSAGES[other]}


class TestClickMeButton:
    @pytest.mark.parametrize(
        "key",
        [
            pytest.param(Keys.ENTER, id="enter"),
            pytest.param(Keys.SPACE, id="space"),
        ],
    )
    def test_keyboard_activates_click_me(self, buttons_page, key):
        buttons_page.press_key_on_button("Click Me", key)

        message = buttons_page.wait_for_message("Click Me")
        assert message == EXPECTED_MESSAGES["Click Me"]

    def test_click_me_works_after_a_refresh(self, buttons_page):
        buttons_page.driver.refresh()

        buttons_page.click_button("Click Me")

        message = buttons_page.wait_for_message("Click Me")
        assert message == EXPECTED_MESSAGES["Click Me"]


class TestButtonsRefresh:
    def test_refreshing_the_page_clears_the_messages(self, buttons_page):
        buttons_page.click_button("Click Me")
        assert buttons_page.wait_for_message("Click Me")

        buttons_page.driver.refresh()

        assert buttons_page.button_labels()
        assert buttons_page.messages() == {}


class TestButtonsKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the header moves after loading, so content jumps.",
    )
    def test_content_stays_in_place_after_loading(self, buttons_page):
        assert buttons_page.layout_shift_score() == 0
