import re

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.dynamic_properties_page import (
    DynamicPropertiesPage,
)
from playwright_tests.pages.elements_page import ElementsPage
from playwright_tests.pages.home_page import HomePage

pytestmark = pytest.mark.regression

WHITE = "rgb(255, 255, 255)"
RED = "rgb(220, 53, 69)"
CHANGE_TIMEOUT_MS = DynamicPropertiesPage.CHANGE_TIMEOUT_MS


@pytest.fixture
def dynamic_properties_page(open_page):
    return open_page(DynamicPropertiesPage)


class TestDynamicPropertiesNavigation:
    @pytest.mark.smoke
    def test_dynamic_properties_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_elements()
        expect(page).to_have_url("https://demoqa.com/elements")

        elements_page = ElementsPage(page)
        elements_page.go_to_dynamic_properties()
        expect(page).to_have_url("https://demoqa.com/dynamic-properties")
        expect(elements_page.heading).to_have_text("Dynamic Properties")


class TestEnableAfter:
    def test_button_is_disabled_at_first(self, dynamic_properties_page):
        expect(dynamic_properties_page.enable_after_button).to_be_disabled()

    @pytest.mark.smoke
    def test_button_becomes_enabled(self, dynamic_properties_page):
        expect(dynamic_properties_page.enable_after_button).to_be_enabled(
            timeout=CHANGE_TIMEOUT_MS
        )


class TestColorChange:
    def test_text_is_white_at_first(self, dynamic_properties_page):
        expect(dynamic_properties_page.color_change_button).to_have_css(
            "color", WHITE
        )

    def test_text_turns_red(self, dynamic_properties_page):
        expect(dynamic_properties_page.color_change_button).to_have_css(
            "color", RED, timeout=CHANGE_TIMEOUT_MS
        )


class TestVisibleAfter:
    def test_button_is_hidden_at_first(self, dynamic_properties_page):
        # Wait for the page's content first, so "hidden" is not just
        # "not drawn yet".
        expect(dynamic_properties_page.color_change_button).to_be_visible()
        expect(dynamic_properties_page.visible_after_button).to_be_hidden()

    def test_button_appears(self, dynamic_properties_page):
        expect(dynamic_properties_page.visible_after_button).to_be_visible(
            timeout=CHANGE_TIMEOUT_MS
        )


class TestRandomId:
    def test_text_has_five_character_id(self, dynamic_properties_page):
        expect(dynamic_properties_page.random_id_text).to_have_id(
            re.compile(r"^[A-Za-z0-9]{5}$")
        )

    def test_id_changes_on_reload(self, dynamic_properties_page):
        first_id = dynamic_properties_page.random_id_text.get_attribute("id")

        dynamic_properties_page.reload()

        expect(dynamic_properties_page.random_id_text).not_to_have_id(
            first_id
        )
