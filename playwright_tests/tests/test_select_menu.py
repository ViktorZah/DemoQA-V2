import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.select_menu_page import SelectMenuPage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

SELECT_VALUE_OPTIONS = [
    "Group 1, option 1",
    "Group 1, option 2",
    "Group 2, option 1",
    "Group 2, option 2",
    "A root option",
    "Another root option",
]
TITLES = ["Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "Other"]
MULTI_COLOURS = ["Green", "Blue", "Black", "Red"]
# "Violet" is misspelled "Voilet" (a known bug), so passing tests leave it
# out and only the xfail checks it.
OLD_SELECT_COLOUR_COUNT = 11
CARS = ["Volvo", "Saab", "Opel", "Audi"]


@pytest.fixture
def select_menu_page(open_page):
    return open_page(SelectMenuPage)


class TestSelectMenuNavigation:
    @pytest.mark.smoke
    def test_select_menu_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_select_menu()
        expect(page).to_have_url("https://demoqa.com/select-menu")
        expect(widgets_page.heading).to_have_text("Select Menu")


class TestSelectValue:
    def test_shows_placeholder_at_first(self, select_menu_page):
        expect(select_menu_page.placeholder("Select Value")).to_have_text(
            "Select Option"
        )

    def test_offers_grouped_options(self, select_menu_page):
        select_menu_page.open_options("Select Value")

        expect(select_menu_page.group_headings).to_have_text(
            ["Group 1", "Group 2"]
        )
        expect(select_menu_page.options).to_have_text(SELECT_VALUE_OPTIONS)

    @pytest.mark.parametrize(
        "option",
        [
            pytest.param("Group 2, option 1", marks=pytest.mark.smoke),
            "A root option",
        ],
    )
    def test_chosen_option_is_shown(self, select_menu_page, option):
        select_menu_page.choose("Select Value", option)

        expect(select_menu_page.chosen("Select Value")).to_have_text(option)
        expect(select_menu_page.options).to_have_count(0)

    def test_choosing_again_replaces_the_option(self, select_menu_page):
        select_menu_page.choose("Select Value", "A root option")
        expect(select_menu_page.chosen("Select Value")).to_have_text(
            "A root option"
        )

        select_menu_page.choose("Select Value", "Group 1, option 2")

        expect(select_menu_page.chosen("Select Value")).to_have_text(
            "Group 1, option 2"
        )


class TestSelectOne:
    def test_shows_placeholder_at_first(self, select_menu_page):
        expect(select_menu_page.placeholder("Select One")).to_have_text(
            "Select Title"
        )

    def test_offers_titles(self, select_menu_page):
        select_menu_page.open_options("Select One")

        expect(select_menu_page.group_headings).to_have_text(
            ["Pick one title"]
        )
        expect(select_menu_page.options).to_have_text(TITLES)

    def test_chosen_title_is_shown(self, select_menu_page):
        select_menu_page.choose("Select One", "Prof.")

        expect(select_menu_page.chosen("Select One")).to_have_text("Prof.")


class TestOldStyleSelect:
    def test_starts_on_red_with_eleven_colours(self, select_menu_page):
        expect(select_menu_page.old_select_chosen).to_have_text("Red")
        expect(select_menu_page.old_select_options).to_have_count(
            OLD_SELECT_COLOUR_COUNT
        )

    def test_chosen_colour_is_selected(self, select_menu_page):
        select_menu_page.choose_old_select("Purple")

        expect(select_menu_page.old_select_chosen).to_have_text("Purple")


class TestMultiselect:
    def test_shows_placeholder_at_first(self, select_menu_page):
        expect(select_menu_page.multi_placeholder).to_have_text("Select...")
        expect(select_menu_page.chosen_colours).to_have_count(0)

    def test_offers_four_colours(self, select_menu_page):
        select_menu_page.open_multi_options()

        expect(select_menu_page.options).to_have_text(MULTI_COLOURS)

    @pytest.mark.smoke
    def test_chosen_colours_are_all_shown(self, select_menu_page):
        select_menu_page.choose_colours("Green", "Black")

        expect(select_menu_page.chosen_colours).to_have_text(
            ["Green", "Black"]
        )

    def test_chosen_colours_leave_the_list(self, select_menu_page):
        select_menu_page.choose_colours("Green", "Black")

        select_menu_page.open_multi_options()

        expect(select_menu_page.options).to_have_text(["Blue", "Red"])

    def test_remove_button_removes_that_colour(self, select_menu_page):
        select_menu_page.choose_colours("Green", "Blue", "Black")

        select_menu_page.remove_colour("Blue")

        expect(select_menu_page.chosen_colours).to_have_text(
            ["Green", "Black"]
        )

    def test_backspace_removes_the_last_colour(self, select_menu_page):
        select_menu_page.choose_colours("Green", "Black")

        select_menu_page.press_in_multi_field("Backspace")

        expect(select_menu_page.chosen_colours).to_have_text(["Green"])


class TestStandardMultiSelect:
    def test_lists_four_cars(self, select_menu_page):
        expect(select_menu_page.car_options).to_have_text(CARS)

    def test_several_cars_can_be_selected(self, select_menu_page):
        select_menu_page.choose_cars("Saab", "Audi")

        expect(select_menu_page.cars).to_have_values(["saab", "audi"])


class TestSelectMenuKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the old style select misspells \"Violet\" as "
            "\"Voilet\"."
        ),
    )
    def test_old_select_spells_violet_correctly(self, select_menu_page):
        expect(
            select_menu_page.old_select_options.filter(has_text="Violet")
        ).to_have_count(1, timeout=2_000)
