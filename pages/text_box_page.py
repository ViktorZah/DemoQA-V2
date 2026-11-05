from collections import Counter

from selenium.webdriver.common.by import By

from pages.elements_page import ElementsPage


class TextBoxPage(ElementsPage):
    PATH = "/text-box"

    FULL_NAME_INPUT = (By.ID, "userName")
    EMAIL_INPUT = (By.ID, "userEmail")
    SUBMIT_BUTTON = (By.ID, "submit")

    # The site reuses these two ids on the output lines, so scope them by tag.
    CURRENT_ADDRESS_INPUT = (By.CSS_SELECTOR, "textarea#currentAddress")
    PERMANENT_ADDRESS_INPUT = (By.CSS_SELECTOR, "textarea#permanentAddress")

    ANY_OUTPUT_LINE = (By.CSS_SELECTOR, "#output p")
    OUTPUT_LINES = {
        "full_name": (By.CSS_SELECTOR, "#output p#name"),
        "email": (By.CSS_SELECTOR, "#output p#email"),
        "current_address": (By.CSS_SELECTOR, "#output p#currentAddress"),
        "permanent_address": (By.CSS_SELECTOR, "#output p#permanentAddress"),
    }

    FORM_ELEMENTS_WITH_ID = (By.CSS_SELECTOR, "#userForm [id]")

    FIELD_ERROR_CLASS = "field-error"

    def fill_form(
        self,
        full_name: str = "",
        email: str = "",
        current_address: str = "",
        permanent_address: str = "",
    ) -> None:
        self.type_text(self.FULL_NAME_INPUT, full_name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.CURRENT_ADDRESS_INPUT, current_address)
        self.type_text(self.PERMANENT_ADDRESS_INPUT, permanent_address)

    def submit(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    def email_has_error(self) -> bool:
        """Return whether the email field is marked invalid right now."""
        field = self.find_visible(self.EMAIL_INPUT)
        return self.FIELD_ERROR_CLASS in field.get_attribute("class").split()

    def wait_for_email_error(self) -> bool:
        """Return whether the email field becomes marked invalid in time."""
        return self.wait_until(lambda _: self.email_has_error())

    def output(self) -> dict[str, str]:
        """Return the values shown right now, without their labels.

        Use this to check that no output appears. Use wait_for_output()
        when output is expected.
        """
        values = {}
        for field, locator in self.OUTPUT_LINES.items():
            for line in self.driver.find_elements(*locator):
                values[field] = line.text.split(":", 1)[1].strip()
        return values

    def wait_for_output(self) -> dict[str, str]:
        """Wait for output to appear, then return its values."""
        self.find_all_visible(self.ANY_OUTPUT_LINE)
        return self.output()

    def wait_for_output_to_be(
        self, expected: dict[str, str]
    ) -> dict[str, str]:
        """Wait for existing output to change, then return its values."""
        self.wait_until(lambda _: self.output() == expected)
        return self.output()

    def duplicate_form_ids(self) -> list[str]:
        """Return the ids used by more than one element in the form."""
        elements = self.driver.find_elements(*self.FORM_ELEMENTS_WITH_ID)
        counts = Counter(element.get_attribute("id") for element in elements)
        return [element_id for element_id, n in counts.items() if n > 1]

    def output_label(self, field: str) -> str:
        """Return the label shown in front of a submitted value."""
        line = self.find_visible(self.OUTPUT_LINES[field])
        return line.text.split(":", 1)[0].strip()
