import re
from datetime import date

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.widgets.date_picker_page import DatePickerPage
from playwright_tests.pages.widgets.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

TWELVE_HOUR_TIME = re.compile(r"\d{1,2}:\d\d (AM|PM)$")


@pytest.fixture
def date_picker_page(open_page):
    return open_page(DatePickerPage)


class TestDatePickerNavigation:
    @pytest.mark.smoke
    def test_date_picker_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_date_picker()
        expect(page).to_have_url("https://demoqa.com/date-picker")
        expect(widgets_page.heading).to_have_text("Date Picker")


class TestDatePickerInitialState:
    def test_date_field_shows_today(self, date_picker_page):
        expect(date_picker_page.field("date")).to_have_value(
            date.today().strftime("%m/%d/%Y")
        )

    def test_date_and_time_field_shows_today_and_a_time(
        self, date_picker_page
    ):
        today = date.today()
        expected = re.compile(
            rf"^{today:%B} {today.day}, {today.year} \d{{1,2}}:\d\d (AM|PM)$"
        )

        expect(date_picker_page.field("date_time")).to_have_value(expected)


class TestDateField:
    @pytest.mark.smoke
    def test_chosen_date_is_shown(self, date_picker_page):
        date_picker_page.choose_date(date(1990, 5, 15))

        expect(date_picker_page.field("date")).to_have_value("05/15/1990")
        expect(date_picker_page.calendar("date")).to_be_hidden()

    def test_month_buttons_move_one_month(self, date_picker_page):
        date_picker_page.choose_date(date(1990, 5, 15))
        date_picker_page.open_calendar("date")
        expect(date_picker_page.calendar_month("date")).to_have_text(
            "May 1990"
        )

        date_picker_page.go_to_next_month("date")
        expect(date_picker_page.calendar_month("date")).to_have_text(
            "June 1990"
        )

        date_picker_page.go_to_previous_month("date")
        date_picker_page.go_to_previous_month("date")
        expect(date_picker_page.calendar_month("date")).to_have_text(
            "April 1990"
        )

    def test_typed_date_is_accepted(self, date_picker_page):
        date_picker_page.type_date("12/25/2020")

        expect(date_picker_page.field("date")).to_have_value("12/25/2020")

    @pytest.mark.parametrize(
        "typed",
        ["not a date", "02/30/2021", "13/01/2021"],
        ids=["text", "impossible_day", "impossible_month"],
    )
    def test_invalid_typed_date_keeps_previous_date(
        self, date_picker_page, typed
    ):
        date_picker_page.type_date("12/25/2020")
        expect(date_picker_page.field("date")).to_have_value("12/25/2020")

        date_picker_page.type_date(typed)

        expect(date_picker_page.field("date")).to_have_value("12/25/2020")


class TestDateAndTimeField:
    @pytest.mark.smoke
    def test_chosen_date_and_time_are_shown(self, date_picker_page):
        date_picker_page.choose_date_and_time(date(2024, 3, 10), "14:30")

        expect(date_picker_page.field("date_time")).to_have_value(
            "March 10, 2024 2:30 PM"
        )

    def test_times_are_offered_every_fifteen_minutes(self, date_picker_page):
        date_picker_page.open_calendar("date_time")

        times = date_picker_page.time_options.all_text_contents()

        assert len(times) == 96
        assert times[:3] == ["00:00", "00:15", "00:30"]
        assert times[-1] == "23:45"


class TestDatePickerKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the time list uses a 24-hour clock (14:30), but the "
            "field shows a 12-hour time (2:30 PM)."
        ),
    )
    def test_time_list_and_field_use_same_clock(self, date_picker_page):
        date_picker_page.open_calendar("date_time")

        first_option = date_picker_page.time_options.first.text_content()
        field_value = date_picker_page.field("date_time").input_value()

        # Either clock is fine, as long as both use the same one.
        option_is_12_hour = bool(TWELVE_HOUR_TIME.search(first_option))
        field_is_12_hour = bool(TWELVE_HOUR_TIME.search(field_value))
        assert option_is_12_hour == field_is_12_hour
