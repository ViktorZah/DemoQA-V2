import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.tool_tips_page import ToolTipsPage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

TOOLTIP_TEXTS = {
    "button": "You hovered over the Button",
    "text field": "You hovered over the text field",
    "Contrary": "You hovered over the Contrary",
    "1.10.32": "You hovered over the 1.10.32",
}


@pytest.fixture
def tool_tips_page(open_page):
    return open_page(ToolTipsPage)


class TestToolTipsNavigation:
    @pytest.mark.smoke
    def test_tool_tips_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_tool_tips()
        expect(page).to_have_url("https://demoqa.com/tool-tips")
        expect(widgets_page.heading).to_have_text("Tool Tips")


class TestToolTipsHover:
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("button", marks=pytest.mark.smoke),
            "text field",
            "Contrary",
            "1.10.32",
        ],
    )
    def test_hover_shows_its_tooltip(self, tool_tips_page, name):
        tool_tips_page.hover(name)

        expect(tool_tips_page.tooltip).to_have_text(TOOLTIP_TEXTS[name])
        # Screen readers read the tooltip as the target's description.
        expect(tool_tips_page.target(name)).to_have_accessible_description(
            TOOLTIP_TEXTS[name]
        )

    def test_moving_mouse_away_hides_tooltip(self, tool_tips_page):
        tool_tips_page.hover("button")
        expect(tool_tips_page.tooltip).to_be_visible()

        tool_tips_page.move_mouse_away()

        expect(tool_tips_page.tooltip).to_have_count(0)

    def test_only_the_hovered_tooltip_is_shown(self, tool_tips_page):
        tool_tips_page.hover("button")
        expect(tool_tips_page.tooltip).to_have_text(TOOLTIP_TEXTS["button"])

        tool_tips_page.hover("text field")

        # The new tooltip appears after about 0.3s, and the old one takes
        # about 0.8s to go, so both show for a moment. Wait for each.
        new_tip = tool_tips_page.tooltip_saying(TOOLTIP_TEXTS["text field"])
        old_tip = tool_tips_page.tooltip_saying(TOOLTIP_TEXTS["button"])
        expect(new_tip).to_be_visible()
        expect(old_tip).to_have_count(0)
        expect(tool_tips_page.tooltip).to_have_count(1)


class TestToolTipsKeyboard:
    @pytest.mark.parametrize("name", ["button", "text field"])
    def test_focus_shows_its_tooltip(self, tool_tips_page, name):
        tool_tips_page.focus(name)

        expect(tool_tips_page.tooltip).to_have_text(TOOLTIP_TEXTS[name])
