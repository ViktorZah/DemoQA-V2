import re
from datetime import date

import pytest
from playwright.sync_api import Page, expect

from playwright_tests.pages.forms_page import FormsPage
from playwright_tests.pages.home_page import HomePage
from playwright_tests.pages.practice_form_page import PracticeFormPage

pytestmark = pytest.mark.regression

RED = "rgb(220, 53, 69)"
GREEN = "rgb(25, 135, 84)"
# Known bugs are checked with a short limit, as their outcome shows at once.
QUICK_TIMEOUT_MS = 2_000

REQUIRED = {
    "first_name": "Jane",
    "last_name": "Doe",
    "gender": "Female",
    "mobile": "0123456789",
}
# Misspelled cities are left out, so fixing them will not break this. They
# are checked in the known bugs below.
CITIES = {
    "NCR": ["Delhi", "Gurgaon", "Noida"],
    "Uttar Pradesh": ["Agra", "Lucknow"],
    "Haryana": ["Karnal", "Panipat"],
    "Rajasthan": ["Jaipur"],
}


@pytest.fixture
def practice_form_page(open_page):
    return open_page(PracticeFormPage)


@pytest.fixture
def picture(tmp_path):
    path = tmp_path / "photo.jpg"
    path.write_bytes(b"Not a real image, only its name is shown.")
    return path


class TestPracticeFormNavigation:
    @pytest.mark.smoke
    def test_practice_form_is_reached_from_home_page(self, page: Page):
        home_page = HomePage(page)
        home_page.open()

        home_page.go_to_forms()
        expect(page).to_have_url("https://demoqa.com/forms")

        forms_page = FormsPage(page)
        forms_page.go_to_practice_form()
        expect(page).to_have_url(
            "https://demoqa.com/automation-practice-form"
        )
        expect(forms_page.heading).to_have_text("Practice Form")


class TestPracticeFormInitialState:
    def test_form_title_is_shown(self, practice_form_page):
        expect(practice_form_page.form_title).to_have_text(
            "Student Registration Form"
        )

    def test_date_of_birth_is_today_at_first(self, practice_form_page):
        expect(practice_form_page.field("date_of_birth")).to_have_value(
            date.today().strftime("%d %b %Y")
        )

    def test_city_is_disabled_until_state_is_chosen(self, practice_form_page):
        expect(practice_form_page.city_field).to_be_disabled()

        practice_form_page.choose_state("NCR")

        expect(practice_form_page.city_field).to_be_enabled()


class TestPracticeFormSubmission:
    @pytest.mark.smoke
    def test_required_fields_alone_are_accepted(self, practice_form_page):
        practice_form_page.fill_form(**REQUIRED)
        practice_form_page.submit()

        expect(practice_form_page.result_title).to_have_text(
            "Thanks for submitting the form"
        )
        values = practice_form_page.result_values()
        assert values["Student Name"] == "Jane Doe"
        assert values["Gender"] == "Female"
        assert values["Mobile"] == "0123456789"

    def test_every_field_is_shown_in_result(
        self, practice_form_page, picture
    ):
        practice_form_page.fill_form(
            **REQUIRED,
            email="jane.doe@example.com",
            date_of_birth=date(1990, 5, 15),
            subjects=["Maths", "English"],
            hobbies=["Sports", "Music"],
            picture=picture,
            current_address="1 Main St\nSpringfield",
            state="Haryana",
            city="Karnal",
        )
        practice_form_page.submit()

        expect(practice_form_page.result).to_be_visible()
        values = practice_form_page.result_values()
        # The date is checked on its own, as its format has a known bug.
        assert re.fullmatch(r"15 May, ?1990", values.pop("Date of Birth"))
        assert values == {
            "Student Name": "Jane Doe",
            "Student Email": "jane.doe@example.com",
            "Gender": "Female",
            "Mobile": "0123456789",
            "Subjects": "Maths, English",
            "Hobbies": "Sports, Music",
            "Picture": "photo.jpg",
            "Address": "1 Main St\nSpringfield",
            "State and City": "Haryana Karnal",
        }


class TestPracticeFormValidation:
    @pytest.mark.parametrize(
        "field", ["first_name", "last_name", "mobile"]
    )
    def test_missing_required_text_field_blocks_submission(
        self, practice_form_page, field
    ):
        practice_form_page.fill_form(**{**REQUIRED, field: ""})
        practice_form_page.submit()

        expect(practice_form_page.field(field)).to_have_css(
            "border-color", RED
        )
        expect(practice_form_page.result).to_have_count(0)

    def test_missing_gender_blocks_submission(self, practice_form_page):
        values = {**REQUIRED}
        del values["gender"]
        practice_form_page.fill_form(**values)
        practice_form_page.submit()

        for gender in ["Male", "Female", "Other"]:
            expect(practice_form_page.gender_label(gender)).to_have_css(
                "color", RED
            )
        expect(practice_form_page.result).to_have_count(0)

    @pytest.mark.parametrize(
        "mobile", ["012345678", "abcdefghij"], ids=["nine_digits", "letters"]
    )
    def test_invalid_mobile_blocks_submission(
        self, practice_form_page, mobile
    ):
        practice_form_page.fill_form(**{**REQUIRED, "mobile": mobile})
        practice_form_page.submit()

        expect(practice_form_page.field("mobile")).to_have_css(
            "border-color", RED
        )
        expect(practice_form_page.result).to_have_count(0)

    def test_mobile_keeps_only_ten_digits(self, practice_form_page):
        practice_form_page.field("mobile").press_sequentially("012345678901")

        expect(practice_form_page.field("mobile")).to_have_value(
            "0123456789"
        )

    def test_invalid_email_blocks_submission(self, practice_form_page):
        practice_form_page.fill_form(**REQUIRED, email="not-an-email")
        practice_form_page.submit()

        expect(practice_form_page.field("email")).to_have_css(
            "border-color", RED
        )
        expect(practice_form_page.result).to_have_count(0)


class TestPracticeFormSubjects:
    def test_typing_suggests_matching_subject(self, practice_form_page):
        practice_form_page.type_subject("Ma")

        expect(practice_form_page.suggestions).to_have_text(["Maths"])


class TestPracticeFormCities:
    @pytest.mark.parametrize("state", CITIES)
    def test_state_offers_its_cities(self, practice_form_page, state):
        practice_form_page.choose_state(state)
        practice_form_page.open_city_list()

        expect(practice_form_page.suggestions.first).to_be_visible()
        cities = practice_form_page.suggestions.all_text_contents()
        assert set(CITIES[state]) <= set(cities)


class TestPracticeFormResultClosing:
    def test_escape_closes_result(self, practice_form_page):
        practice_form_page.fill_form(**REQUIRED)
        practice_form_page.submit()
        expect(practice_form_page.result).to_be_visible()

        practice_form_page.close_result_with_escape()

        expect(practice_form_page.result).to_have_count(0)

    def test_clicking_outside_closes_result(self, practice_form_page):
        practice_form_page.fill_form(**REQUIRED)
        practice_form_page.submit()
        expect(practice_form_page.result).to_be_visible()

        practice_form_page.click_outside_result()

        expect(practice_form_page.result).to_have_count(0)


class TestPracticeFormKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: the result's Close button does nothing. Clicking it "
            "throws 'findDOMNode is not a function'."
        ),
    )
    def test_close_button_closes_result(self, practice_form_page):
        practice_form_page.fill_form(**REQUIRED)
        practice_form_page.submit()
        practice_form_page.result.wait_for()

        practice_form_page.close_result()

        expect(practice_form_page.result).to_have_count(
            0, timeout=QUICK_TIMEOUT_MS
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason=(
            "Site bug: rejects valid emails containing + or an apostrophe, "
            "or ending in a domain longer than five letters."
        ),
    )
    @pytest.mark.parametrize(
        "email",
        [
            "jane+tag@example.com",
            "o'neil@example.com",
            "jane@example.museum",
        ],
    )
    def test_valid_email_is_accepted(self, practice_form_page, email):
        practice_form_page.fill_form(**REQUIRED, email=email)
        practice_form_page.submit()

        expect(practice_form_page.field("email")).to_have_css(
            "border-color", GREEN, timeout=QUICK_TIMEOUT_MS
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: a name of only spaces is accepted.",
    )
    @pytest.mark.parametrize("field", ["first_name", "last_name"])
    def test_name_of_only_spaces_is_rejected(self, practice_form_page, field):
        practice_form_page.fill_form(**{**REQUIRED, field: "   "})
        practice_form_page.submit()

        expect(practice_form_page.field(field)).to_have_css(
            "border-color", RED, timeout=QUICK_TIMEOUT_MS
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: spaces around names are kept in the result.",
    )
    def test_result_name_has_no_extra_spaces(self, practice_form_page):
        practice_form_page.fill_form(
            **{**REQUIRED, "first_name": "  Jane  ", "last_name": " Doe "}
        )
        practice_form_page.submit()
        practice_form_page.result.wait_for()

        assert practice_form_page.result_values()["Student Name"] == (
            "Jane Doe"
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: a date of birth in the future is accepted.",
    )
    def test_future_date_of_birth_is_rejected(self, practice_form_page):
        practice_form_page.fill_form(
            **REQUIRED, date_of_birth=date(2030, 1, 15)
        )
        practice_form_page.submit()

        expect(practice_form_page.field("date_of_birth")).to_have_css(
            "border-color", RED, timeout=QUICK_TIMEOUT_MS
        )

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the result's date has no space after the comma.",
    )
    def test_result_date_has_space_after_comma(self, practice_form_page):
        practice_form_page.fill_form(
            **REQUIRED, date_of_birth=date(1990, 5, 15)
        )
        practice_form_page.submit()
        practice_form_page.result.wait_for()

        date_of_birth = practice_form_page.result_values()["Date of Birth"]
        assert not re.search(r",\S", date_of_birth)

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: city names are misspelled.",
    )
    @pytest.mark.parametrize(
        ("state", "city"),
        [("Uttar Pradesh", "Meerut"), ("Rajasthan", "Jaisalmer")],
    )
    def test_city_is_spelled_correctly(self, practice_form_page, state, city):
        practice_form_page.choose_state(state)
        practice_form_page.open_city_list()
        practice_form_page.suggestions.first.wait_for()

        assert city in practice_form_page.suggestions.all_text_contents()

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: changing the state keeps the other state's city.",
    )
    def test_changing_state_clears_city(self, practice_form_page):
        practice_form_page.choose_state("Rajasthan")
        practice_form_page.choose_city("Jaipur")
        practice_form_page.selected_city.wait_for()

        practice_form_page.choose_state("NCR")

        expect(practice_form_page.selected_city).to_have_count(
            0, timeout=QUICK_TIMEOUT_MS
        )
