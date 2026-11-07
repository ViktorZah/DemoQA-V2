import re
from datetime import date

from playwright.sync_api import Locator

from playwright_tests.pages.calendar import choose_with_dropdowns, day_cell
from playwright_tests.pages.widgets_page import WidgetsPage


class DatePickerPage(WidgetsPage):
    """A date field and a date-and-time field, each with a calendar."""

    PATH = "/date-picker"

    # The fields are not tied to their labels, so they are found by ID.
    FIELDS = {
        "date": "#datePickerMonthYearInput",
        "date_time": "#dateAndTimePickerInput",
    }
    CALENDARS = {"date": "Choose Date", "date_time": "Choose Date and Time"}

    def field(self, kind: str) -> Locator:
        return self.page.locator(self.FIELDS[kind])

    def calendar(self, kind: str) -> Locator:
        return self.page.get_by_role(
            "dialog", name=self.CALENDARS[kind], exact=True
        )

    def calendar_month(self, kind: str) -> Locator:
        """The month and year shown at the top of the calendar."""
        return self.calendar(kind).get_by_role("heading", level=2)

    def open_calendar(self, kind: str) -> None:
        self.field(kind).click()
        self.calendar(kind).wait_for()

    def choose_date(self, day: date) -> None:
        self.open_calendar("date")
        choose_with_dropdowns(self.page, day)

    def go_to_next_month(self, kind: str) -> None:
        self.calendar(kind).get_by_role("button", name="Next Month").click()

    def go_to_previous_month(self, kind: str) -> None:
        self.calendar(kind).get_by_role(
            "button", name="Previous Month"
        ).click()

    def type_date(self, text: str) -> None:
        """Replace the date by typing, then leave the field."""
        field = self.field("date")
        field.click()
        field.press("ControlOrMeta+a")
        field.press_sequentially(text)
        field.press("Enter")
        self.heading.click()

    @property
    def time_options(self) -> Locator:
        return self.calendar("date_time").get_by_role("option")

    def choose_date_and_time(self, day: date, time: str) -> None:
        """Pick a day and a time such as "14:30" in the second calendar.

        Its month and year are lists that open from buttons, and its year
        list shows only a few years around the current one.
        """
        self.open_calendar("date_time")
        calendar = self.calendar("date_time")
        calendar.locator(".react-datepicker__month-read-view").click()
        calendar.locator(".react-datepicker__month-option").filter(
            has_text=re.compile(rf"{day:%B}$")
        ).click()
        calendar.locator(".react-datepicker__year-read-view").click()
        calendar.locator(".react-datepicker__year-option").filter(
            has_text=re.compile(rf"^(✓\s*)?{day.year}$")
        ).click()
        day_cell(self.page, day).click()
        calendar.get_by_role("option", name=time, exact=True).click()
