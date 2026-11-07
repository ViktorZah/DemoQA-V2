import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage
from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.modal_dialogs_page import ModalDialogsPage

pytestmark = pytest.mark.regression

# The start of each body. The small one's full text has known bugs.
BODY_STARTS = {
    "small": "This is a small modal.",
    "large": "Lorem Ipsum is simply dummy text",
}
WIDTHS = {"small": 300, "large": 800}


@pytest.fixture
def modal_dialogs_page(open_page):
    return open_page(ModalDialogsPage)


class TestModalDialogsNavigation:
    @pytest.mark.smoke
    def test_modal_dialogs_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_alerts_frame_and_windows()
        expect(page).to_have_url("https://demoqa.com/alertsWindows")

        section_page = AlertsWindowsPage(page)
        section_page.go_to_modal_dialogs()
        expect(page).to_have_url("https://demoqa.com/modal-dialogs")
        expect(section_page.heading).to_have_text("Modal Dialogs")


class TestModalDialogsInitialState:
    def test_intro_and_both_buttons_are_shown(self, modal_dialogs_page):
        expect(modal_dialogs_page.intro).to_be_visible()
        for size in ModalDialogsPage.MODALS:
            expect(modal_dialogs_page.open_button(size)).to_be_visible()

    def test_no_dialog_is_open_at_first(self, modal_dialogs_page):
        expect(modal_dialogs_page.intro).to_be_visible()
        expect(modal_dialogs_page.any_dialog).to_have_count(0)


class TestModalDialogsOpening:
    @pytest.mark.parametrize(
        "size", [pytest.param("small", marks=pytest.mark.smoke), "large"]
    )
    def test_button_opens_its_dialog(self, modal_dialogs_page, size):
        modal_dialogs_page.open_button(size).click()

        expect(modal_dialogs_page.dialog(size)).to_be_visible()
        expect(modal_dialogs_page.body(size)).to_contain_text(
            BODY_STARTS[size]
        )

    @pytest.mark.parametrize("size", ModalDialogsPage.MODALS)
    def test_dialog_has_its_width(self, modal_dialogs_page, size):
        modal_dialogs_page.open_modal(size)

        assert modal_dialogs_page.dialog_width(size) == WIDTHS[size]


class TestModalDialogsClosing:
    @pytest.mark.parametrize("way", ["footer", "x", "escape", "outside"])
    @pytest.mark.parametrize("size", ModalDialogsPage.MODALS)
    def test_dialog_closes(self, modal_dialogs_page, size, way):
        modal_dialogs_page.open_modal(size)

        modal_dialogs_page.close(size, way)

        expect(modal_dialogs_page.any_dialog).to_have_count(0)


class TestModalDialogsKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the small dialog says 'very less content'.",
    )
    def test_small_dialog_text_is_grammatical(self, modal_dialogs_page):
        modal_dialogs_page.open_modal("small")

        assert "very less" not in modal_dialogs_page.body("small").inner_text()

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the small dialog's text has no final full stop.",
    )
    def test_small_dialog_text_ends_with_full_stop(self, modal_dialogs_page):
        modal_dialogs_page.open_modal("small")

        assert modal_dialogs_page.body("small").inner_text().endswith(".")
