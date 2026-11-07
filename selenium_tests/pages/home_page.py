from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    SECTION_CARD_TITLES = (By.CSS_SELECTOR, ".category-cards .card-body h5")
    ELEMENTS_CARD = (By.CSS_SELECTOR, ".category-cards a[href='/elements']")

    def section_names(self) -> list[str]:
        cards = self.find_all_visible(self.SECTION_CARD_TITLES)
        return [card.text for card in cards]

    def go_to_elements(self) -> None:
        self.click(self.ELEMENTS_CARD)
