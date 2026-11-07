import re

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.accordion_page import AccordionPage
from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

SECTIONS = AccordionPage.SECTIONS
BODY_STARTS = {
    "What is Lorem Ipsum?": "Lorem Ipsum is simply dummy text",
    "Where does it come from?": "Contrary to popular belief",
    "Why do we use it?": "It is a long established fact",
}
# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000


@pytest.fixture
def accordion_page(open_page):
    return open_page(AccordionPage)


def expect_only_open(accordion_page, open_section):
    """Check that only the given section is open, or none if None."""
    for section in SECTIONS:
        button = accordion_page.section_button(section)
        body = accordion_page.section_body(section)
        if section == open_section:
            expect(button).to_have_attribute("aria-expanded", "true")
            expect(body).to_be_visible()
        else:
            expect(button).to_have_attribute("aria-expanded", "false")
            expect(body).to_be_hidden()


class TestAccordionNavigation:
    @pytest.mark.smoke
    def test_accordion_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_accordion()
        expect(page).to_have_url("https://demoqa.com/accordian")
        # Either spelling, so fixing the known typo will not break this.
        expect(widgets_page.heading).to_have_text(
            re.compile(r"^Accordi[ao]n$")
        )


class TestAccordionInitialState:
    def test_all_sections_are_shown(self, accordion_page):
        expect(accordion_page.section_buttons).to_have_text(SECTIONS)

    def test_only_first_section_is_open_at_first(self, accordion_page):
        expect_only_open(accordion_page, SECTIONS[0])

    def test_first_section_shows_its_text(self, accordion_page):
        expect(accordion_page.section_body(SECTIONS[0])).to_contain_text(
            BODY_STARTS[SECTIONS[0]]
        )


class TestAccordionToggling:
    @pytest.mark.parametrize(
        "section",
        [pytest.param(SECTIONS[1], marks=pytest.mark.smoke), SECTIONS[2]],
    )
    def test_opening_a_section_closes_the_others(
        self, accordion_page, section
    ):
        accordion_page.toggle(section)

        expect_only_open(accordion_page, section)
        expect(accordion_page.section_body(section)).to_contain_text(
            BODY_STARTS[section]
        )

    def test_clicking_open_section_closes_it(self, accordion_page):
        accordion_page.toggle(SECTIONS[0])

        expect_only_open(accordion_page, None)

    def test_closed_section_opens_again(self, accordion_page):
        accordion_page.toggle(SECTIONS[0])
        expect_only_open(accordion_page, None)

        accordion_page.toggle(SECTIONS[0])

        expect_only_open(accordion_page, SECTIONS[0])

    @pytest.mark.parametrize("key", ["Enter", " "], ids=["enter", "space"])
    def test_keyboard_toggles_section(self, accordion_page, key):
        accordion_page.press_key_on(SECTIONS[2], key)
        expect_only_open(accordion_page, SECTIONS[2])

        accordion_page.press_key_on(SECTIONS[2], key)

        expect_only_open(accordion_page, None)


class TestAccordionKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the heading misspells 'Accordion' as 'Accordian'.",
    )
    def test_heading_is_spelled_correctly(self, accordion_page):
        expect(accordion_page.heading).to_have_text(
            "Accordion", timeout=QUICK_TIMEOUT_MS
        )
