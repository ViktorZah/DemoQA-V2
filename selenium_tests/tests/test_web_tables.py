import pytest

from selenium_tests.pages.elements_page import ElementsPage
from selenium_tests.pages.home_page import HomePage
from selenium_tests.pages.web_tables_page import WebTablesPage

pytestmark = pytest.mark.regression

DEFAULT_NAMES = ["Cierra", "Alden", "Kierra"]
ALDEN = {
    "first_name": "Alden",
    "last_name": "Cantrell",
    "age": "45",
    "email": "alden@example.com",
    "salary": "12000",
    "department": "Compliance",
}
NEW_RECORD = {
    "first_name": "Jane",
    "last_name": "Doe",
    "age": "30",
    "email": "jane@example.com",
    "salary": "5000",
    "department": "QA",
}
FIRST_PAGE_NAMES = DEFAULT_NAMES + [f"User{n}" for n in range(7)]
SECOND_PAGE_NAMES = ["User7", "User8"]


@pytest.fixture
def web_tables_page(open_page):
    return open_page(WebTablesPage)


@pytest.fixture
def page_with_12_records(web_tables_page):
    for number in range(9):
        web_tables_page.add_record(
            **{**NEW_RECORD, "first_name": f"User{number}"}
        )
    return web_tables_page


class TestWebTablesNavigation:
    @pytest.mark.smoke
    def test_web_tables_is_reached_from_home_page(self, driver):
        home_page = HomePage(driver)
        home_page.open()

        home_page.go_to_elements()
        elements_page = ElementsPage(driver)
        assert elements_page.wait_for_url("https://demoqa.com/elements")

        elements_page.go_to_web_tables()
        web_tables_page = WebTablesPage(driver)
        assert web_tables_page.wait_for_url("https://demoqa.com/webtables")
        assert web_tables_page.heading == "Web Tables"


class TestWebTablesInitialState:
    def test_columns_are_shown(self, web_tables_page):
        assert web_tables_page.column_headers() == [
            "First Name",
            "Last Name",
            "Age",
            "Email",
            "Salary",
            "Department",
            "Action",
        ]

    def test_three_default_records_are_shown(self, web_tables_page):
        assert web_tables_page.first_names() == DEFAULT_NAMES
        assert web_tables_page.rows()[1] == ALDEN
        assert web_tables_page.page_indicator == "1 of 1"


class TestWebTablesAddForm:
    def test_add_form_opens_empty(self, web_tables_page):
        web_tables_page.open_add_form()

        assert web_tables_page.form_title() == "Registration Form"
        assert set(web_tables_page.form_values().values()) == {""}

    @pytest.mark.smoke
    def test_adding_a_record_shows_it_last(self, web_tables_page):
        web_tables_page.add_record(**NEW_RECORD)

        assert web_tables_page.wait_for_first_names_to_be(
            DEFAULT_NAMES + ["Jane"]
        ) == DEFAULT_NAMES + ["Jane"]
        assert web_tables_page.rows()[-1] == NEW_RECORD

    def test_closing_the_form_adds_nothing(self, web_tables_page):
        web_tables_page.open_add_form()
        web_tables_page.fill_form(**NEW_RECORD)

        web_tables_page.close_form()

        assert web_tables_page.first_names() == DEFAULT_NAMES

    def test_html_is_shown_as_typed(self, web_tables_page):
        name = "<b>Jane</b>"

        web_tables_page.add_record(**{**NEW_RECORD, "first_name": name})

        shown = web_tables_page.wait_for_first_names_to_be(
            DEFAULT_NAMES + [name]
        )
        assert shown == DEFAULT_NAMES + [name]


class TestWebTablesFormValidation:
    def test_empty_form_is_rejected(self, web_tables_page):
        web_tables_page.open_add_form()

        web_tables_page.submit_form()

        assert web_tables_page.wait_for_form_errors()
        all_fields = list(WebTablesPage.FORM_FIELDS)
        assert web_tables_page.invalid_fields() == all_fields
        assert web_tables_page.first_names() == DEFAULT_NAMES

    @pytest.mark.parametrize("field", NEW_RECORD)
    def test_each_field_is_required(self, web_tables_page, field):
        web_tables_page.open_add_form()
        web_tables_page.fill_form(**{**NEW_RECORD, field: ""})

        web_tables_page.submit_form()

        assert web_tables_page.wait_for_form_errors()
        assert web_tables_page.invalid_fields() == [field]
        assert web_tables_page.first_names() == DEFAULT_NAMES

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("email", "not-an-email"),
            ("age", "abc"),
            ("age", "-1"),
            ("salary", "abc"),
            ("salary", "-5"),
        ],
    )
    def test_invalid_value_is_rejected(self, web_tables_page, field, value):
        web_tables_page.open_add_form()
        web_tables_page.fill_form(**{**NEW_RECORD, field: value})

        web_tables_page.submit_form()

        assert web_tables_page.wait_for_form_errors()
        assert web_tables_page.invalid_fields() == [field]
        assert web_tables_page.first_names() == DEFAULT_NAMES


class TestWebTablesEdit:
    def test_edit_form_shows_the_record(self, web_tables_page):
        web_tables_page.open_edit_form(2)

        assert web_tables_page.form_values() == ALDEN

    @pytest.mark.smoke
    def test_saving_an_edit_changes_only_that_record(self, web_tables_page):
        web_tables_page.open_edit_form(2)
        web_tables_page.fill_form(age="46")

        web_tables_page.submit_form()

        assert web_tables_page.wait_for_form_to_close()
        rows = web_tables_page.rows()
        assert rows[1] == {**ALDEN, "age": "46"}
        assert [row["first_name"] for row in rows] == DEFAULT_NAMES

    def test_closing_an_edit_keeps_the_record(self, web_tables_page):
        web_tables_page.open_edit_form(2)
        web_tables_page.fill_form(age="99")

        web_tables_page.close_form()

        assert web_tables_page.rows()[1] == ALDEN

    def test_invalid_edit_is_rejected(self, web_tables_page):
        web_tables_page.open_edit_form(2)
        web_tables_page.fill_form(email="not-an-email")

        web_tables_page.submit_form()

        assert web_tables_page.wait_for_form_errors()
        assert web_tables_page.invalid_fields() == ["email"]

        web_tables_page.close_form()
        assert web_tables_page.rows()[1] == ALDEN


class TestWebTablesDelete:
    @pytest.mark.smoke
    def test_deleting_a_record_removes_only_that_record(self, web_tables_page):
        web_tables_page.delete_record(2)

        expected = ["Cierra", "Kierra"]
        assert web_tables_page.wait_for_first_names_to_be(expected) == expected

    def test_deleting_an_added_record_removes_it(self, web_tables_page):
        web_tables_page.add_record(**NEW_RECORD)
        web_tables_page.wait_for_first_names_to_be(DEFAULT_NAMES + ["Jane"])

        web_tables_page.delete_record(4)

        shown = web_tables_page.wait_for_first_names_to_be(DEFAULT_NAMES)
        assert shown == DEFAULT_NAMES


class TestWebTablesSearch:
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            pytest.param("cierra", ["Cierra"], id="any_letter_case"),
            pytest.param("Vega", ["Cierra"], id="last_name"),
            pytest.param("39", ["Cierra"], id="age"),
            pytest.param("alden@example.com", ["Alden"], id="email"),
            pytest.param("12000", ["Alden"], id="salary"),
            pytest.param("leg", ["Kierra"], id="part_of_department"),
        ],
    )
    def test_search_finds_matching_records(
        self, web_tables_page, text, expected
    ):
        web_tables_page.search(text)

        shown = web_tables_page.wait_for_first_names_to_be(expected)
        assert shown == expected

    def test_search_with_no_match_shows_no_records(self, web_tables_page):
        web_tables_page.search("no such record")

        assert web_tables_page.wait_for_first_names_to_be([]) == []

    def test_clearing_the_search_shows_every_record(self, web_tables_page):
        web_tables_page.search("Vega")
        web_tables_page.wait_for_first_names_to_be(["Cierra"])

        web_tables_page.clear_search()

        shown = web_tables_page.wait_for_first_names_to_be(DEFAULT_NAMES)
        assert shown == DEFAULT_NAMES


class TestWebTablesPaging:
    def test_next_and_previous_move_between_pages(self, page_with_12_records):
        page = page_with_12_records
        assert page.first_names() == FIRST_PAGE_NAMES
        assert page.page_indicator == "1 of 2"

        page.go_to_page("Next")
        assert page.wait_for_first_names_to_be(
            SECOND_PAGE_NAMES
        ) == SECOND_PAGE_NAMES
        assert page.page_indicator == "2 of 2"

        page.go_to_page("Previous")
        assert page.wait_for_first_names_to_be(
            FIRST_PAGE_NAMES
        ) == FIRST_PAGE_NAMES

    def test_last_and_first_jump_to_the_ends(self, page_with_12_records):
        page = page_with_12_records

        page.go_to_page("Last")
        assert page.wait_for_first_names_to_be(
            SECOND_PAGE_NAMES
        ) == SECOND_PAGE_NAMES

        page.go_to_page("First")
        assert page.wait_for_first_names_to_be(
            FIRST_PAGE_NAMES
        ) == FIRST_PAGE_NAMES

    def test_larger_page_size_shows_every_record(self, page_with_12_records):
        page = page_with_12_records

        page.set_page_size(20)

        expected = FIRST_PAGE_NAMES + SECOND_PAGE_NAMES
        assert page.wait_for_first_names_to_be(expected) == expected
        assert page.page_indicator == "1 of 1"


class TestWebTablesRefresh:
    def test_refreshing_the_page_restores_the_default_records(
        self, web_tables_page
    ):
        web_tables_page.add_record(**NEW_RECORD)
        web_tables_page.wait_for_first_names_to_be(DEFAULT_NAMES + ["Jane"])

        web_tables_page.driver.refresh()

        shown = web_tables_page.wait_for_first_names_to_be(DEFAULT_NAMES)
        assert shown == DEFAULT_NAMES


class TestWebTablesKnownBugs:
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: each delete brings back records deleted earlier.",
    )
    def test_second_delete_keeps_the_first_record_deleted(
        self, web_tables_page
    ):
        web_tables_page.delete_record(1)
        web_tables_page.wait_for_first_names_to_be(["Alden", "Kierra"])

        web_tables_page.delete_record(2)
        web_tables_page.wait_for_first_names_to_be(["Cierra", "Kierra"])

        assert web_tables_page.first_names() == ["Kierra"]

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: deleting any record discards added records.",
    )
    def test_delete_keeps_other_added_records(self, web_tables_page):
        web_tables_page.add_record(**NEW_RECORD)
        web_tables_page.add_record(**{**NEW_RECORD, "first_name": "Sam"})
        web_tables_page.wait_for_first_names_to_be(
            DEFAULT_NAMES + ["Jane", "Sam"]
        )

        web_tables_page.delete_record(4)
        web_tables_page.wait_for_first_names_to_be(DEFAULT_NAMES)

        assert web_tables_page.first_names() == DEFAULT_NAMES + ["Sam"]

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: a value of only spaces is accepted as filled in.",
    )
    @pytest.mark.parametrize(
        "field", ["first_name", "last_name", "department"]
    )
    def test_value_of_only_spaces_is_rejected(self, web_tables_page, field):
        web_tables_page.open_add_form()
        web_tables_page.fill_form(**{**NEW_RECORD, field: "   "})

        web_tables_page.submit_form()

        assert not web_tables_page.wait_for_form_to_close()

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
    def test_valid_email_is_accepted(self, web_tables_page, email):
        web_tables_page.open_add_form()
        web_tables_page.fill_form(**{**NEW_RECORD, "email": email})

        assert web_tables_page.invalid_fields() == []

    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="Site bug: the add form shows the record from a closed edit.",
    )
    def test_add_form_is_empty_after_closing_an_edit(self, web_tables_page):
        web_tables_page.open_edit_form(1)
        web_tables_page.close_form()

        web_tables_page.open_add_form()

        assert set(web_tables_page.form_values().values()) == {""}
