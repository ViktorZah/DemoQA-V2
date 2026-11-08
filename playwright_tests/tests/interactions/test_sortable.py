import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.interactions.interactions_page import (
    InteractionsPage,
)
from playwright_tests.pages.interactions.sortable_page import SortablePage

pytestmark = pytest.mark.regression

LIST = ["One", "Two", "Three", "Four", "Five", "Six"]
GRID = LIST + ["Seven", "Eight", "Nine"]


@pytest.fixture
def sortable_page(open_page):
    return open_page(SortablePage)


class TestSortableNavigation:
    @pytest.mark.smoke
    def test_sortable_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_interactions()
        expect(page).to_have_url("https://demoqa.com/interaction")

        interactions_page = InteractionsPage(page)
        interactions_page.go_to_sortable()
        expect(page).to_have_url("https://demoqa.com/sortable")
        expect(interactions_page.heading).to_have_text("Sortable")


class TestSortableList:
    def test_list_is_shown_in_order_at_first(self, sortable_page):
        expect(sortable_page.tab("List")).to_have_attribute(
            "aria-selected", "true"
        )
        expect(sortable_page.list_items).to_have_text(LIST)

    @pytest.mark.smoke
    def test_item_moved_down_takes_that_place(self, sortable_page):
        sortable_page.move_in_list("One", onto="Three")

        expect(sortable_page.list_items).to_have_text(
            ["Two", "Three", "One", "Four", "Five", "Six"]
        )

    def test_item_moved_up_takes_that_place(self, sortable_page):
        sortable_page.move_in_list("Six", onto="Two")

        expect(sortable_page.list_items).to_have_text(
            ["One", "Six", "Two", "Three", "Four", "Five"]
        )

    def test_new_order_is_kept_after_switching_tabs(self, sortable_page):
        sortable_page.move_in_list("One", onto="Three")
        new_order = ["Two", "Three", "One", "Four", "Five", "Six"]
        expect(sortable_page.list_items).to_have_text(new_order)

        sortable_page.show("Grid")
        sortable_page.show("List")

        expect(sortable_page.list_items).to_have_text(new_order)


class TestSortableGrid:
    def test_grid_is_shown_in_order(self, sortable_page):
        sortable_page.show("Grid")

        expect(sortable_page.grid_items).to_have_text(GRID)

    def test_item_moved_forward_takes_that_place(self, sortable_page):
        sortable_page.show("Grid")

        sortable_page.move_in_grid("One", onto="Five")

        expect(sortable_page.grid_items).to_have_text(
            ["Two", "Three", "Four", "Five", "One", "Six", "Seven", "Eight",
             "Nine"]
        )

    def test_item_moved_back_takes_that_place(self, sortable_page):
        sortable_page.show("Grid")

        sortable_page.move_in_grid("Nine", onto="One")

        expect(sortable_page.grid_items).to_have_text(
            ["Nine", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
             "Eight"]
        )
