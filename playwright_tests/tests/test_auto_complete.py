import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.auto_complete_page import AutoCompletePage
from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000


@pytest.fixture
def auto_complete_page(open_page):
    return open_page(AutoCompletePage)


class TestAutoCompleteNavigation:
    @pytest.mark.smoke
    def test_auto_complete_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_auto_complete()
        expect(page).to_have_url("https://demoqa.com/auto-complete")
        expect(widgets_page.heading).to_have_text("Auto Complete")


class TestAutoCompleteInitialState:
    def test_both_fields_are_empty_at_first(self, auto_complete_page):
        for kind in AutoCompletePage.FIELDS:
            expect(auto_complete_page.field(kind)).to_have_value("")
        expect(auto_complete_page.chosen_colours).to_have_count(0)
        expect(auto_complete_page.single_colour).to_have_count(0)


class TestAutoCompleteSuggestions:
    @pytest.mark.parametrize(
        ("typed", "suggested"),
        [
            ("bl", ["Blue", "Black"]),
            ("RE", ["Red", "Green"]),
            ("a", ["Black", "Magenta", "Aqua"]),
        ],
        ids=["start_of_name", "any_case", "middle_of_name"],
    )
    def test_typing_suggests_matching_colours(
        self, auto_complete_page, typed, suggested
    ):
        auto_complete_page.type_into("multiple", typed)

        expect(auto_complete_page.suggestions).to_have_text(suggested)

    def test_typing_no_match_suggests_nothing(self, auto_complete_page):
        auto_complete_page.type_into("multiple", "bl")
        expect(auto_complete_page.suggestions).to_have_count(2)

        auto_complete_page.type_into("multiple", "xyz")

        expect(auto_complete_page.suggestions).to_have_count(0)

    def test_chosen_colour_is_no_longer_suggested(self, auto_complete_page):
        auto_complete_page.choose("multiple", "Red")

        auto_complete_page.type_into("multiple", "re")

        expect(auto_complete_page.suggestions).to_have_text(["Green"])


class TestAutoCompleteMultiple:
    @pytest.mark.smoke
    def test_several_colours_can_be_chosen(self, auto_complete_page):
        auto_complete_page.choose("multiple", "Red")
        auto_complete_page.choose("multiple", "Blue")

        expect(auto_complete_page.chosen_colours).to_have_text(["Red", "Blue"])

    def test_enter_chooses_highlighted_suggestion(self, auto_complete_page):
        auto_complete_page.type_into("multiple", "Gr")
        expect(auto_complete_page.suggestions).to_have_text(["Green"])

        auto_complete_page.press("multiple", "Enter")

        expect(auto_complete_page.chosen_colours).to_have_text(["Green"])

    def test_remove_button_removes_only_that_colour(self, auto_complete_page):
        auto_complete_page.choose("multiple", "Red")
        auto_complete_page.choose("multiple", "Blue")

        auto_complete_page.remove("Red")

        expect(auto_complete_page.chosen_colours).to_have_text(["Blue"])

    def test_backspace_removes_last_colour(self, auto_complete_page):
        auto_complete_page.choose("multiple", "Red")
        auto_complete_page.choose("multiple", "Blue")

        auto_complete_page.press("multiple", "Backspace")

        expect(auto_complete_page.chosen_colours).to_have_text(["Red"])

    def test_clear_all_removes_every_colour(self, auto_complete_page):
        auto_complete_page.choose("multiple", "Red")
        auto_complete_page.choose("multiple", "Blue")

        auto_complete_page.clear_all()

        expect(auto_complete_page.chosen_colours).to_have_count(0)


class TestAutoCompleteSingle:
    def test_one_colour_can_be_chosen(self, auto_complete_page):
        auto_complete_page.choose("single", "Red")

        expect(auto_complete_page.single_colour).to_have_text("Red")

    def test_new_colour_replaces_previous_one(self, auto_complete_page):
        auto_complete_page.choose("single", "Red")
        expect(auto_complete_page.single_colour).to_have_text("Red")

        auto_complete_page.choose("single", "Blue")

        expect(auto_complete_page.single_colour).to_have_text("Blue")


class TestAutoCompleteKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: 'Violet' is misspelled 'Voilet', so typing 'Vio' "
            "suggests nothing."
        ),
    )
    def test_typing_vio_suggests_violet(self, auto_complete_page):
        auto_complete_page.type_into("multiple", "Vio")

        expect(auto_complete_page.suggestions).to_have_text(
            ["Violet"], timeout=QUICK_TIMEOUT_MS
        )
