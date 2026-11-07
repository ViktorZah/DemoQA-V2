"""Shared actions for the site's pop-up calendar (react-datepicker)."""

import re
from datetime import date

from playwright.sync_api import Locator, Page


def day_cell(page: Page, day: date) -> Locator:
    """Return the calendar cell for a day.

    Each day is named like "Choose Tuesday, May 15th, 1990".
    """
    name = re.compile(rf", {day:%B} {day.day}(st|nd|rd|th), {day.year}$")
    return page.get_by_role("gridcell", name=name)


def choose_with_dropdowns(page: Page, day: date) -> None:
    """Pick a day in an open calendar that has month and year dropdowns."""
    page.locator(".react-datepicker__month-select").select_option(
        label=day.strftime("%B")
    )
    page.locator(".react-datepicker__year-select").select_option(
        str(day.year)
    )
    day_cell(page, day).click()
