import pytest

from pages.elements_page import ElementsPage
from pages.home_page import HomePage
from pages.text_box_page import TextBoxPage

pytestmark = pytest.mark.regression

VALID_FORM = {
    "full_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "current_address": "1 Main Street",
    "permanent_address": "2 Oak Avenue",
}


@pytest.fixture
def text_box_page(open_page):
    return open_page(TextBoxPage)


class TestTextBoxNavigation:
    @pytest.mark.smoke
    def test_text_box_is_reached_from_home_page(self, driver):
        home_page = HomePage(driver)
        home_page.open()

        home_page.go_to_elements()
        elements_page = ElementsPage(driver)
        assert elements_page.wait_for_url("https://demoqa.com/elements")

        elements_page.go_to_text_box()
        text_box_page = TextBoxPage(driver)
        assert text_box_page.wait_for_url("https://demoqa.com/text-box")
        assert text_box_page.heading == "Text Box"


class TestTextBoxSubmission:
    @pytest.mark.smoke
    def test_submitting_all_fields_shows_every_value(self, text_box_page):
        text_box_page.fill_form(**VALID_FORM)
        text_box_page.submit()

        assert text_box_page.wait_for_output() == VALID_FORM

    @pytest.mark.parametrize("field", VALID_FORM)
    def test_submitting_one_field_shows_only_that_value(
        self, text_box_page, field
    ):
        submitted = {field: VALID_FORM[field]}

        text_box_page.fill_form(**submitted)
        text_box_page.submit()

        assert text_box_page.wait_for_output() == submitted

    def test_multiline_address_keeps_all_its_text(self, text_box_page):
        address = "1 Main Street\nApartment 4"

        text_box_page.fill_form(current_address=address)
        text_box_page.submit()

        shown_address = text_box_page.wait_for_output()["current_address"]
        assert shown_address.split() == address.split()

    def test_submitting_empty_form_shows_no_output(self, text_box_page):
        text_box_page.submit()

        assert text_box_page.output() == {}
        assert not text_box_page.email_has_error()

    def test_resubmitting_replaces_previous_output(self, text_box_page):
        first = {"full_name": "First", "email": "first@example.com"}
        second = {"full_name": "Second", "email": "second@example.com"}

        text_box_page.fill_form(**first)
        text_box_page.submit()
        assert text_box_page.wait_for_output() == first

        text_box_page.fill_form(**second)
        text_box_page.submit()

        assert text_box_page.wait_for_output_to_be(second) == second

    def test_clearing_a_field_removes_it_from_output(self, text_box_page):
        name_only = {"full_name": "Jane Doe"}

        text_box_page.fill_form(**VALID_FORM)
        text_box_page.submit()
        assert text_box_page.wait_for_output() == VALID_FORM

        text_box_page.fill_form(**name_only)
        text_box_page.submit()

        assert text_box_page.wait_for_output_to_be(name_only) == name_only


class TestTextBoxInputHandling:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("<b>bold</b>", id="html_tag"),
            pytest.param("<script>window.x=1</script>", id="script_tag"),
            pytest.param("<img src=x onerror=window.x=1>", id="image_tag"),
            pytest.param("O'Brien & Sons \"Ltd\"", id="quotes_ampersand"),
            pytest.param("Jos\u00e9 M\u00fcller", id="accented_letters"),
            pytest.param("\u5317\u4eac", id="chinese_characters"),
            pytest.param("Apt: 4: rear", id="colons"),
            pytest.param("100% $5 #1 \\ / {x}", id="symbols"),
        ],
    )
    def test_special_characters_are_shown_as_typed(
        self, text_box_page, value
    ):
        # Exact text proves HTML was displayed, not rendered or executed.
        submitted = {"full_name": value, "current_address": value}

        text_box_page.fill_form(**submitted)
        text_box_page.submit()

        assert text_box_page.wait_for_output() == submitted

    def test_long_text_is_shown_in_full(self, text_box_page):
        submitted = {"full_name": "a" * 5000, "current_address": "b" * 5000}

        text_box_page.fill_form(**submitted)
        text_box_page.submit()

        assert text_box_page.wait_for_output() == submitted


class TestTextBoxEmailValidation:
    @pytest.mark.parametrize(
        "valid_email",
        [
            "UPPER@EXAMPLE.COM",
            "user_name-1@example.co.uk",
            "123@example.com",
            "jane@sub.example.com",
            "jane@my-site.com",
        ],
    )
    def test_valid_email_is_accepted(self, text_box_page, valid_email):
        text_box_page.fill_form(email=valid_email)
        text_box_page.submit()

        assert text_box_page.wait_for_output() == {"email": valid_email}
        assert not text_box_page.email_has_error()

    def test_spaces_around_email_are_ignored(self, text_box_page):
        text_box_page.fill_form(email="  jane@example.com  ")
        text_box_page.submit()

        assert text_box_page.wait_for_output() == {
            "email": "jane@example.com"
        }
        assert not text_box_page.email_has_error()

    def test_email_of_only_spaces_counts_as_empty(self, text_box_page):
        text_box_page.fill_form(email="   ")
        text_box_page.submit()

        assert text_box_page.output() == {}
        assert not text_box_page.email_has_error()

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "not-an-email",
            "jane@example",
            "jane doe@example.com",
            "@example.com",
            "jane@.com",
            "jane..doe@example.com",
            ".jane@example.com",
            "jane@example..com",
            "jane@example.c",
        ],
    )
    def test_invalid_email_is_rejected(self, text_box_page, invalid_email):
        text_box_page.fill_form(**{**VALID_FORM, "email": invalid_email})
        text_box_page.submit()

        assert text_box_page.wait_for_email_error()
        assert text_box_page.output() == {}

    def test_correcting_invalid_email_allows_submission(self, text_box_page):
        text_box_page.fill_form(**{**VALID_FORM, "email": "not-an-email"})
        text_box_page.submit()
        assert text_box_page.wait_for_email_error()

        text_box_page.fill_form(**VALID_FORM)
        text_box_page.submit()

        assert text_box_page.wait_for_output() == VALID_FORM
        assert not text_box_page.email_has_error()


class TestTextBoxKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: output label is misspelled 'Permananet Address'.",
    )
    def test_permanent_address_label_is_spelled_correctly(self, text_box_page):
        text_box_page.fill_form(**VALID_FORM)
        text_box_page.submit()

        label = text_box_page.output_label("permanent_address")
        assert label == "Permanent Address"

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: a rejected submission keeps the previous output.",
    )
    def test_rejected_submission_clears_previous_output(self, text_box_page):
        text_box_page.fill_form(**VALID_FORM)
        text_box_page.submit()

        text_box_page.fill_form(**{**VALID_FORM, "email": "not-an-email"})
        text_box_page.submit()

        assert text_box_page.output() == {}

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: rejects valid emails containing + or an apostrophe, "
            "or ending in a domain longer than three letters."
        ),
    )
    @pytest.mark.parametrize(
        "valid_email",
        [
            "jane+tag@example.com",
            "o'neil@example.com",
            "jane@example.info",
        ],
    )
    def test_commonly_rejected_valid_email_is_accepted(
        self, text_box_page, valid_email
    ):
        text_box_page.fill_form(email=valid_email)
        text_box_page.submit()

        assert not text_box_page.email_has_error()
        assert text_box_page.output() == {"email": valid_email}

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: a value of only spaces is shown as a blank line.",
    )
    @pytest.mark.parametrize(
        "field", ["full_name", "current_address", "permanent_address"]
    )
    def test_value_of_only_spaces_counts_as_empty(self, text_box_page, field):
        text_box_page.fill_form(**{field: "   "})
        text_box_page.submit()

        assert text_box_page.output() == {}

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: output lines reuse the address input ids.",
    )
    def test_form_ids_are_unique_after_submitting(self, text_box_page):
        text_box_page.fill_form(**VALID_FORM)
        text_box_page.submit()
        text_box_page.wait_for_output()

        assert text_box_page.duplicate_form_ids() == []
