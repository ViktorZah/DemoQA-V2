from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.elements_page import ElementsPage


class LinksPage(ElementsPage):
    PATH = "/links"

    ALL_LINKS = (By.CSS_SELECTOR, "#linkWrapper a")
    NEW_TAB_LINKS = {
        "simple": (By.ID, "simpleLink"),
        # Its text is "Home" plus random characters, new on every load.
        "dynamic": (By.ID, "dynamicLink"),
    }
    API_LINKS = {
        "Created": (By.ID, "created"),
        "No Content": (By.ID, "no-content"),
        "Moved": (By.ID, "moved"),
        "Bad Request": (By.ID, "bad-request"),
        "Unauthorized": (By.ID, "unauthorized"),
        "Forbidden": (By.ID, "forbidden"),
        "Not Found": (By.ID, "invalid-url"),
    }
    RESPONSE = (By.ID, "linkResponse")
    # The message shows the status code and text in bold.
    RESPONSE_VALUES = (By.CSS_SELECTOR, "#linkResponse b")
    RESPONSE_STATUS_CODE = (By.CSS_SELECTOR, "#linkResponse b:first-of-type")

    def link_labels(self) -> list[str]:
        links = self.find_all_visible(self.ALL_LINKS)
        return [link.text for link in links]

    def new_tab_link_text(self, link: str) -> str:
        return self.find_visible(self.NEW_TAB_LINKS[link]).text

    def click_new_tab_link(self, link: str) -> None:
        self.click(self.NEW_TAB_LINKS[link])

    def click_api_link(self, link: str) -> None:
        self.click(self.API_LINKS[link])

    def response_message(self) -> str | None:
        """Return the response message shown right now, if any."""
        elements = self.driver.find_elements(*self.RESPONSE)
        return elements[0].text if elements else None

    def wait_for_response(self, status_code: str) -> bool:
        """Wait for the message to show the given status code."""
        return self.wait_until(
            EC.text_to_be_present_in_element(
                self.RESPONSE_STATUS_CODE, status_code
            )
        )

    def response_values(self) -> list[str]:
        """Return the status code and text shown in the message."""
        values = self.driver.find_elements(*self.RESPONSE_VALUES)
        return [value.text for value in values]
