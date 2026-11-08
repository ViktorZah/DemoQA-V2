import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.interactions.interactions_page import (
    InteractionsPage,
)
from playwright_tests.pages.interactions.selectable_page import SelectablePage

pytestmark = pytest.mark.regression

LIST = [
    "Cras justo odio",
    "Dapibus ac facilisis in",
    "Morbi leo risus",
    "Porta ac consectetur ac",
]
GRID = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
        "Nine"]
BLUE = "rgb(13, 110, 253)"
WHITE = "rgb(255, 255, 255)"


@pytest.fixture
def selectable_page(open_page):
    return open_page(SelectablePage)


class TestSelectableNavigation:
    @pytest.mark.smoke
    def test_selectable_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_interactions()
        expect(page).to_have_url("https://demoqa.com/interaction")

        interactions_page = InteractionsPage(page)
        interactions_page.go_to_selectable()
        expect(page).to_have_url("https://demoqa.com/selectable")
        expect(interactions_page.heading).to_have_text("Selectable")


class TestSelectableList:
    def test_list_shows_four_items_none_selected(self, selectable_page):
        expect(selectable_page.list_items).to_have_text(LIST)
        expect(selectable_page.selected_list_items).to_have_count(0)

    @pytest.mark.smoke
    def test_clicking_item_selects_it_in_blue(self, selectable_page):
        selectable_page.click_list_item("Morbi leo risus")
        selectable_page.move_mouse_away()

        expect(selectable_page.selected_list_items).to_have_text(
            ["Morbi leo risus"]
        )
        expect(selectable_page.list_item("Morbi leo risus")).to_have_css(
            "background-color", BLUE
        )

    def test_several_items_can_be_selected(self, selectable_page):
        selectable_page.click_list_item("Cras justo odio")
        selectable_page.click_list_item("Porta ac consectetur ac")

        expect(selectable_page.selected_list_items).to_have_text(
            ["Cras justo odio", "Porta ac consectetur ac"]
        )

    def test_clicking_selected_item_deselects_it(self, selectable_page):
        selectable_page.click_list_item("Cras justo odio")
        expect(selectable_page.selected_list_items).to_have_count(1)

        selectable_page.click_list_item("Cras justo odio")
        selectable_page.move_mouse_away()

        expect(selectable_page.selected_list_items).to_have_count(0)
        expect(selectable_page.list_item("Cras justo odio")).to_have_css(
            "background-color", WHITE
        )

    def test_selection_is_kept_after_switching_tabs(self, selectable_page):
        selectable_page.click_list_item("Morbi leo risus")
        expect(selectable_page.selected_list_items).to_have_count(1)

        selectable_page.show("Grid")
        selectable_page.show("List")

        expect(selectable_page.selected_list_items).to_have_text(
            ["Morbi leo risus"]
        )


class TestSelectableGrid:
    def test_grid_shows_nine_items_none_selected(self, selectable_page):
        selectable_page.show("Grid")

        expect(selectable_page.grid_items).to_have_text(GRID)
        expect(selectable_page.selected_grid_items).to_have_count(0)

    def test_clicking_grid_items_selects_them(self, selectable_page):
        selectable_page.show("Grid")

        selectable_page.click_grid_item("Five")
        selectable_page.click_grid_item("Nine")

        expect(selectable_page.selected_grid_items).to_have_text(
            ["Five", "Nine"]
        )
