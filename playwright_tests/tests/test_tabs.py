import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.tabs_page import TabsPage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

TAB_NAMES = ["What", "Origin", "Use", "More"]
ENABLED_TABS = ["What", "Origin", "Use"]

# The opening words of each enabled tab's text.
PANEL_STARTS = {
    "What": "Lorem Ipsum is simply dummy text",
    "Origin": "Contrary to popular belief",
    "Use": "It is a long established fact",
}


@pytest.fixture
def tabs_page(open_page):
    return open_page(TabsPage)


def expect_selected(tabs_page, name):
    """Check only this tab is selected, and only its panel is shown."""
    for tab_name in TAB_NAMES:
        selected = "true" if tab_name == name else "false"
        expect(tabs_page.tab(tab_name)).to_have_attribute(
            "aria-selected", selected
        )
    expect(tabs_page.shown_panels).to_have_count(1)
    expect(tabs_page.panel(name)).to_contain_text(PANEL_STARTS[name])


class TestTabsNavigation:
    @pytest.mark.smoke
    def test_tabs_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_tabs()
        expect(page).to_have_url("https://demoqa.com/tabs")
        expect(widgets_page.heading).to_have_text("Tabs")


class TestTabsInitialState:
    def test_four_tabs_are_shown_in_order(self, tabs_page):
        expect(tabs_page.tabs).to_have_text(TAB_NAMES)

    def test_what_is_selected_at_first(self, tabs_page):
        expect_selected(tabs_page, "What")


class TestTabsSwitching:
    @pytest.mark.parametrize(
        "name",
        [pytest.param("Origin", marks=pytest.mark.smoke), "Use"],
    )
    def test_clicking_tab_shows_its_panel(self, tabs_page, name):
        tabs_page.select(name)

        expect_selected(tabs_page, name)

    def test_clicking_first_tab_again_shows_it_again(self, tabs_page):
        tabs_page.select("Use")
        expect_selected(tabs_page, "Use")

        tabs_page.select("What")

        expect_selected(tabs_page, "What")

    def test_clicking_selected_tab_keeps_it_selected(self, tabs_page):
        tabs_page.select("Origin")
        tabs_page.select("Origin")

        expect_selected(tabs_page, "Origin")


class TestTabsKeyboard:
    @pytest.mark.parametrize(
        ("start", "key", "end"),
        [
            ("What", "ArrowRight", "Origin"),
            ("Origin", "ArrowLeft", "What"),
            # The arrows wrap around and skip the disabled More tab.
            ("Use", "ArrowRight", "What"),
            ("What", "ArrowLeft", "Use"),
        ],
    )
    def test_arrow_key_selects_next_tab(self, tabs_page, start, key, end):
        tabs_page.select(start)

        tabs_page.press_on_tab(start, key)

        expect_selected(tabs_page, end)
        expect(tabs_page.tab(end)).to_be_focused()


class TestTabsDisabled:
    def test_more_tab_is_disabled(self, tabs_page):
        expect(tabs_page.tab("More")).to_be_disabled()
        for name in ENABLED_TABS:
            expect(tabs_page.tab(name)).to_be_enabled()
