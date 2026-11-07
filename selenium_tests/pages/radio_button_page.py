from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import Locator
from selenium_tests.pages.elements_page import ElementsPage


class RadioButtonPage(ElementsPage):
    PATH = "/radio-button"

    OPTION_IDS = {
        "Yes": "yesRadio",
        "Impressive": "impressiveRadio",
        "No": "noRadio",
    }

    QUESTION = (By.CSS_SELECTOR, ".mb-3")
    OPTION_LABELS = (By.CSS_SELECTOR, "label.form-check-label")
    RESULT_VALUE = (By.CSS_SELECTOR, ".text-success")
    RESULT_MESSAGE = (By.CSS_SELECTOR, ":has(> .text-success)")

    def _input(self, option: str) -> Locator:
        return (By.ID, self.OPTION_IDS[option])

    def _label(self, option: str) -> Locator:
        return (By.CSS_SELECTOR, f"label[for='{self.OPTION_IDS[option]}']")

    @property
    def question(self) -> str:
        return self.find_visible(self.QUESTION).text

    def option_labels(self) -> list[str]:
        labels = self.find_all_visible(self.OPTION_LABELS)
        return [label.text for label in labels]

    def select(self, option: str) -> None:
        """Click an option's label, as a user would."""
        self.click(self._label(option))

    def is_selected(self, option: str) -> bool:
        return self.find_visible(self._input(option)).is_selected()

    def is_enabled(self, option: str) -> bool:
        return self.find_visible(self._input(option)).is_enabled()

    def selected_options(self) -> list[str]:
        return [
            option for option in self.OPTION_IDS if self.is_selected(option)
        ]

    def result(self) -> str | None:
        """Return the selected value shown right now, if there is one."""
        values = self.driver.find_elements(*self.RESULT_VALUE)
        return values[0].text if values else None

    def wait_for_result_to_be(self, expected: str) -> str | None:
        """Wait for the shown value to appear or change, then return it."""
        self.wait_until(lambda _: self.result() == expected)
        return self.result()

    @property
    def result_message(self) -> str:
        return self.find_visible(self.RESULT_MESSAGE).text
