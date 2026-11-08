import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.menu_page import MenuPage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

MAIN_ITEMS = ["Main Item 1", "Main Item 2", "Main Item 3"]
SUB_SUB_ITEMS = ["Sub Sub Item 1", "Sub Sub Item 2"]
# The two "Sub Item" entries share a name (a known bug), so passing tests
# only check how many there are and where the sub sub list is.
SUB_ITEM_COUNT = 3
SUB_SUB_LIST = "SUB SUB LIST »"


@pytest.fixture
def menu_page(open_page):
    return open_page(MenuPage)


class TestMenuNavigation:
    @pytest.mark.smoke
    def test_menu_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_menu()
        expect(page).to_have_url("https://demoqa.com/menu")
        expect(widgets_page.heading).to_have_text("Menu")


class TestMenuInitialState:
    def test_only_main_items_are_shown_at_first(self, menu_page):
        expect(menu_page.shown(menu_page.main_items)).to_have_text(
            MAIN_ITEMS
        )
        expect(menu_page.shown(menu_page.sub_items)).to_have_count(0)
        expect(menu_page.shown(menu_page.sub_sub_items)).to_have_count(0)


class TestMenuHover:
    @pytest.mark.smoke
    def test_hovering_main_item_2_shows_its_sub_items(self, menu_page):
        menu_page.hover_main_item("Main Item 2")

        shown_sub_items = menu_page.shown(menu_page.sub_items)
        expect(shown_sub_items).to_have_count(SUB_ITEM_COUNT)
        expect(shown_sub_items.last).to_have_text(SUB_SUB_LIST)
        expect(menu_page.shown(menu_page.sub_sub_items)).to_have_count(0)

    def test_hovering_sub_sub_list_shows_its_items(self, menu_page):
        menu_page.open_sub_sub_list()

        expect(menu_page.shown(menu_page.sub_sub_items)).to_have_text(
            SUB_SUB_ITEMS
        )

    def test_moving_mouse_away_closes_the_menu(self, menu_page):
        menu_page.open_sub_sub_list()
        expect(menu_page.shown(menu_page.sub_sub_items)).to_have_count(2)

        menu_page.move_mouse_away()

        expect(menu_page.shown(menu_page.sub_items)).to_have_count(0)
        expect(menu_page.shown(menu_page.sub_sub_items)).to_have_count(0)


class TestMenuKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: two items under Main Item 2 are both named "
            "\"Sub Item\", so they cannot be told apart."
        ),
    )
    def test_sub_item_names_are_different(self, menu_page):
        names = menu_page.sub_item_names()

        # Any fix is fine, as long as no two names are the same.
        assert len(set(names)) == len(names), names
