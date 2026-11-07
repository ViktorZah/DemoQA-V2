import time

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.alerts_page import AlertsPage, PopUp
from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage
from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression


@pytest.fixture
def alerts_page(open_page):
    return open_page(AlertsPage)


class TestAlertsNavigation:
    @pytest.mark.smoke
    def test_alerts_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_alerts_frame_and_windows()
        expect(page).to_have_url("https://demoqa.com/alertsWindows")

        section_page = AlertsWindowsPage(page)
        section_page.go_to_alerts()
        expect(page).to_have_url("https://demoqa.com/alerts")
        expect(section_page.heading).to_have_text("Alerts")


class TestAlertsInitialState:
    def test_every_button_has_its_description(self, alerts_page):
        expect(alerts_page.rows).to_contain_text(
            list(AlertsPage.DESCRIPTIONS.values())
        )

    def test_no_result_is_shown_at_first(self, alerts_page):
        expect(alerts_page.rows.first).to_be_visible()
        expect(alerts_page.confirm_result).to_have_count(0)
        expect(alerts_page.prompt_result).to_have_count(0)


class TestAlert:
    @pytest.mark.smoke
    def test_alert_shows_its_message(self, alerts_page):
        shown = alerts_page.click_and_answer("alert")

        assert shown == PopUp("alert", "You clicked a button")

    def test_timed_alert_appears_after_five_seconds(self, alerts_page):
        started = time.monotonic()

        shown = alerts_page.click_and_answer("timer")

        waited = time.monotonic() - started
        assert shown == PopUp("alert", "This alert appeared after 5 seconds")
        # Measured at 5.02 seconds. The upper limit leaves room for a slow
        # machine without accepting a much longer delay.
        assert 5 <= waited < 7


class TestConfirm:
    def test_confirm_asks_its_question(self, alerts_page):
        shown = alerts_page.click_and_answer("confirm")

        assert shown == PopUp("confirm", "Do you confirm action?")

    @pytest.mark.parametrize(
        ("accept", "result"),
        [(True, "You selected Ok"), (False, "You selected Cancel")],
        ids=["ok", "cancel"],
    )
    def test_answer_is_shown(self, alerts_page, accept, result):
        alerts_page.click_and_answer("confirm", accept=accept)

        expect(alerts_page.confirm_result).to_have_text(result)


class TestPrompt:
    def test_prompt_asks_for_name(self, alerts_page):
        shown = alerts_page.click_and_answer("prompt", text="Jane Doe")

        assert shown == PopUp("prompt", "Please enter your name")

    @pytest.mark.smoke
    def test_entered_name_is_shown(self, alerts_page):
        alerts_page.click_and_answer("prompt", text="Jane Doe")

        expect(alerts_page.prompt_result).to_have_text("You entered Jane Doe")

    @pytest.mark.parametrize(
        ("accept", "text"),
        [(True, ""), (False, None)],
        ids=["empty_name", "cancel"],
    )
    def test_no_name_shows_no_result(self, alerts_page, accept, text):
        alerts_page.click_and_answer("prompt", accept=accept, text=text)

        # A confirm answer shows its result at once, so once it is shown,
        # the prompt has had its chance to show one too.
        alerts_page.click_and_answer("confirm")
        expect(alerts_page.confirm_result).to_be_visible()
        expect(alerts_page.prompt_result).to_have_count(0)
