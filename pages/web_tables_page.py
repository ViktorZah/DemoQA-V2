from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import Locator
from pages.elements_page import ElementsPage


class WebTablesPage(ElementsPage):
    PATH = "/webtables"

    ADD_BUTTON = (By.ID, "addNewRecordButton")
    SEARCH_BOX = (By.ID, "searchBox")
    COLUMN_HEADERS = (By.CSS_SELECTOR, ".web-tables-wrapper thead th")
    ROWS = (By.CSS_SELECTOR, ".web-tables-wrapper tbody tr")
    CELLS = (By.CSS_SELECTOR, "td")

    FORM = (By.ID, "userForm")
    FORM_TITLE = (By.ID, "registration-form-modal")
    FORM_CLOSE_BUTTON = (By.CSS_SELECTOR, ".modal-content .btn-close")
    SUBMIT_BUTTON = (By.ID, "submit")
    VALIDATED_FORM = (By.CSS_SELECTOR, "#userForm.was-validated")
    FORM_FIELDS = {
        "first_name": "firstName",
        "last_name": "lastName",
        "email": "userEmail",
        "age": "age",
        "salary": "salary",
        "department": "department",
    }
    # The table's column order differs from the form's field order.
    ROW_FIELDS = (
        "first_name",
        "last_name",
        "age",
        "email",
        "salary",
        "department",
    )

    PAGE_INDICATOR = (By.CSS_SELECTOR, ".pagination strong")
    PAGE_SIZE_SELECT = (By.CSS_SELECTOR, ".pagination select")
    PAGING_BUTTON_POSITIONS = {"First": 1, "Previous": 2, "Next": 3, "Last": 4}

    def _field(self, name: str) -> Locator:
        return (By.ID, self.FORM_FIELDS[name])

    def _paging_button(self, name: str) -> Locator:
        position = self.PAGING_BUTTON_POSITIONS[name]
        return (
            By.CSS_SELECTOR,
            f".pagination .btn-group button:nth-child({position})",
        )

    def column_headers(self) -> list[str]:
        headers = self.find_all_visible(self.COLUMN_HEADERS)
        return [header.text for header in headers]

    def rows(self) -> list[dict[str, str]]:
        """Return the records shown right now."""
        records = []
        for row in self.driver.find_elements(*self.ROWS):
            cells = row.find_elements(*self.CELLS)
            values = [cell.text for cell in cells]
            records.append(dict(zip(self.ROW_FIELDS, values)))
        return records

    def first_names(self) -> list[str]:
        return [record["first_name"] for record in self.rows()]

    def wait_for_first_names_to_be(self, expected: list[str]) -> list[str]:
        """Wait for the shown rows to change, then return their first names."""
        self.wait_until(lambda _: self.first_names() == expected)
        return self.first_names()

    def open_add_form(self) -> None:
        self.click(self.ADD_BUTTON)
        self.find_visible(self.FORM)

    def open_edit_form(self, record_id: int) -> None:
        self.click((By.ID, f"edit-record-{record_id}"))
        self.find_visible(self.FORM)

    def form_title(self) -> str:
        return self.find_visible(self.FORM_TITLE).text

    def form_values(self) -> dict[str, str]:
        return {
            name: self.find_visible(self._field(name)).get_attribute("value")
            for name in self.FORM_FIELDS
        }

    def fill_form(self, **fields: str) -> None:
        for name, value in fields.items():
            self.type_text(self._field(name), value)

    def submit_form(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    def close_form(self) -> None:
        self.click(self.FORM_CLOSE_BUTTON)
        self.wait_for_form_to_close()

    def wait_for_form_to_close(self) -> bool:
        return self.wait_until(EC.invisibility_of_element_located(self.FORM))

    def wait_for_form_errors(self) -> bool:
        """Return whether the form starts showing validation errors in time."""
        return self.wait_until(
            EC.presence_of_element_located(self.VALIDATED_FORM)
        )

    def invalid_fields(self) -> list[str]:
        """Return the form fields whose current values are invalid."""
        return [
            name
            for name, field_id in self.FORM_FIELDS.items()
            if self.driver.find_elements(
                By.CSS_SELECTOR, f"#{field_id}:invalid"
            )
        ]

    def add_record(self, **fields: str) -> None:
        self.open_add_form()
        self.fill_form(**fields)
        self.submit_form()
        self.wait_for_form_to_close()

    def delete_record(self, record_id: int) -> None:
        self.click((By.ID, f"delete-record-{record_id}"))

    def search(self, text: str) -> None:
        self.type_text(self.SEARCH_BOX, text)

    def clear_search(self) -> None:
        """Delete the text with Backspace, as a user would.

        Selenium's clear() empties the box without updating the results.
        """
        box = self.find_visible(self.SEARCH_BOX)
        box.send_keys(Keys.BACKSPACE * len(box.get_attribute("value")))

    @property
    def page_indicator(self) -> str:
        return self.find_visible(self.PAGE_INDICATOR).text

    def go_to_page(self, button: str) -> None:
        """Click First, Previous, Next or Last."""
        self.click(self._paging_button(button))

    def set_page_size(self, size: int) -> None:
        select = self.find_visible(self.PAGE_SIZE_SELECT)
        Select(select).select_by_value(str(size))
