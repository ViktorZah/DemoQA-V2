from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ElementsPage(BasePage):
    PATH = "/elements"

    TEXT_BOX_MENU_ITEM = (By.CSS_SELECTOR, ".menu-list a[href='/text-box']")

    def go_to_text_box(self) -> None:
        self.click(self.TEXT_BOX_MENU_ITEM)
