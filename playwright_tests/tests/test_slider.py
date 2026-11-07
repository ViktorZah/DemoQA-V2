import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.slider_page import SliderPage
from playwright_tests.pages.widgets_page import WidgetsPage

pytestmark = pytest.mark.regression

# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000


@pytest.fixture
def slider_page(open_page):
    return open_page(SliderPage)


def expect_value_shown(slider_page, value):
    """Check the slider, the box, the tooltip and aria-valuenow agree."""
    expect(slider_page.slider).to_have_value(str(value))
    expect(slider_page.slider).to_have_attribute("aria-valuenow", str(value))
    expect(slider_page.value_box).to_have_value(str(value))
    expect(slider_page.tooltip).to_have_text(str(value))


class TestSliderNavigation:
    @pytest.mark.smoke
    def test_slider_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_widgets()
        expect(page).to_have_url("https://demoqa.com/widgets")

        widgets_page = WidgetsPage(page)
        widgets_page.go_to_slider()
        expect(page).to_have_url("https://demoqa.com/slider")
        expect(widgets_page.heading).to_have_text("Slider")


class TestSliderInitialState:
    def test_slider_starts_at_25(self, slider_page):
        expect_value_shown(slider_page, 25)

    def test_slider_runs_from_0_to_100(self, slider_page):
        expect(slider_page.slider).to_have_attribute("min", "0")
        expect(slider_page.slider).to_have_attribute("max", "100")


class TestSliderMoving:
    @pytest.mark.smoke
    def test_set_value_is_shown_everywhere(self, slider_page):
        slider_page.set_value(73)

        expect_value_shown(slider_page, 73)

    @pytest.mark.parametrize(
        ("key", "value"),
        [("ArrowRight", 26), ("ArrowLeft", 24), ("Home", 0), ("End", 100)],
    )
    def test_key_moves_slider(self, slider_page, key, value):
        slider_page.press_on_slider(key)

        expect_value_shown(slider_page, value)

    @pytest.mark.parametrize(
        ("edge", "value"), [("left", 0), ("right", 100)]
    )
    def test_clicking_track_edge_moves_slider_there(
        self, slider_page, edge, value
    ):
        slider_page.click_slider_edge(edge)

        expect_value_shown(slider_page, value)


class TestSliderKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: Enter in the value box submits the page's form, which "
            "reloads the page and resets the slider to 25."
        ),
    )
    def test_enter_in_value_box_keeps_slider_value(self, slider_page):
        slider_page.set_value(60)
        expect_value_shown(slider_page, 60)

        slider_page.press_enter_in_value_box()

        expect(slider_page.slider).to_have_value(
            "60", timeout=QUICK_TIMEOUT_MS
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the value box looks editable, but typing in it "
            "changes nothing."
        ),
    )
    def test_value_box_is_read_only_or_moves_slider(self, slider_page):
        expect_value_shown(slider_page, 25)

        slider_page.type_in_value_box("80")

        # Either fix is fine: the box moves the slider, or it cannot be
        # edited at all.
        moved = slider_page.slider.input_value() == "80"
        assert moved or slider_page.value_box_is_read_only()
