from datetime import date
from pathlib import Path

from playwright.sync_api import Locator

from playwright_tests.pages.calendar import choose_with_dropdowns
from playwright_tests.pages.forms.forms_page import FormsPage


class PracticeFormPage(FormsPage):
    """The Student Registration Form.

    The text fields are not tied to their visible labels, so they are found
    by placeholder. Fields with neither use their ID.
    """

    PATH = "/automation-practice-form"

    TEXT_FIELDS = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "name@example.com",
        "mobile": "Mobile Number",
        "current_address": "Current Address",
    }

    @property
    def form(self) -> Locator:
        return self.page.locator("#userForm")

    @property
    def form_title(self) -> Locator:
        return self.page.get_by_role("heading", level=5)

    def field(self, name: str) -> Locator:
        """Return a text field, or the date of birth field."""
        if name == "date_of_birth":
            return self.page.locator("#dateOfBirthInput")
        return self.page.get_by_placeholder(self.TEXT_FIELDS[name], exact=True)

    def gender(self, name: str) -> Locator:
        return self.page.get_by_role("radio", name=name, exact=True)

    def gender_label(self, name: str) -> Locator:
        return self.form.get_by_text(name, exact=True)

    def hobby(self, name: str) -> Locator:
        return self.page.get_by_role("checkbox", name=name, exact=True)

    @property
    def subjects_field(self) -> Locator:
        return self.page.locator("#subjectsInput")

    @property
    def suggestions(self) -> Locator:
        """The options shown by an open subject, state or city list."""
        return self.page.get_by_role("option")

    @property
    def city_field(self) -> Locator:
        return self.page.locator("#city input")

    @property
    def selected_city(self) -> Locator:
        return self.page.locator("#city [class$='-singleValue']")

    @property
    def result(self) -> Locator:
        return self.page.get_by_role("dialog")

    @property
    def result_title(self) -> Locator:
        return self.page.locator("#example-modal-sizes-title-lg")

    def choose_date_of_birth(self, day: date) -> None:
        self.field("date_of_birth").click()
        choose_with_dropdowns(self.page, day)

    def type_subject(self, text: str) -> None:
        # Click first: after a date is chosen, the date picker keeps the
        # focus, and the subjects field clears text typed without focus.
        self.subjects_field.click()
        self.subjects_field.fill(text)

    def add_subject(self, subject: str) -> None:
        self.type_subject(subject)
        self.page.get_by_role("option", name=subject, exact=True).click()

    def choose_state(self, state: str) -> None:
        self.page.locator("#state").click()
        self.page.get_by_role("option", name=state, exact=True).click()

    def choose_city(self, city: str) -> None:
        self.open_city_list()
        self.page.get_by_role("option", name=city, exact=True).click()

    def open_city_list(self) -> None:
        self.page.locator("#city").click()

    def fill_form(self, **values) -> None:
        """Fill the given fields, leaving the others as they are.

        Text fields take a string, gender a name, subjects and hobbies a
        list, date_of_birth a date and picture a file path.
        """
        for name in self.TEXT_FIELDS:
            if name in values:
                self.field(name).fill(values[name])
        if "gender" in values:
            self.gender(values["gender"]).check()
        if "date_of_birth" in values:
            self.choose_date_of_birth(values["date_of_birth"])
        for subject in values.get("subjects", []):
            self.add_subject(subject)
        for hobby in values.get("hobbies", []):
            self.hobby(hobby).check()
        if "picture" in values:
            self.upload_picture(values["picture"])
        if "state" in values:
            self.choose_state(values["state"])
        if "city" in values:
            self.choose_city(values["city"])

    def upload_picture(self, file: Path) -> None:
        self.page.locator("#uploadPicture").set_input_files(file)

    def submit(self) -> None:
        """Click Submit and wait for the form to check its fields."""
        self.page.get_by_role("button", name="Submit", exact=True).click()
        self.page.locator("#userForm.was-validated").wait_for(state="attached")

    def result_values(self) -> dict[str, str]:
        """Return the submitted values shown in the result, by label."""
        rows = self.result.locator("tbody tr")
        values = {}
        for row in rows.all():
            label, value = row.locator("td").all_text_contents()
            values[label] = value
        return values

    def close_result(self) -> None:
        self.page.get_by_role("button", name="Close", exact=True).click()

    def close_result_with_escape(self) -> None:
        self.page.keyboard.press("Escape")

    def click_outside_result(self) -> None:
        # The result covers the page with a backdrop, so any point beside
        # the dialog box lands on it.
        self.page.mouse.click(30, 540)
