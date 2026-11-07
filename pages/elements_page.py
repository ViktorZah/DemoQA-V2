from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ElementsPage(BasePage):
    PATH = "/elements"

    HEADING = (By.TAG_NAME, "h1")
    TEXT_BOX_MENU_ITEM = (By.CSS_SELECTOR, ".menu-list a[href='/text-box']")
    CHECK_BOX_MENU_ITEM = (By.CSS_SELECTOR, ".menu-list a[href='/checkbox']")
    RADIO_BUTTON_MENU_ITEM = (
        By.CSS_SELECTOR,
        ".menu-list a[href='/radio-button']",
    )
    WEB_TABLES_MENU_ITEM = (By.CSS_SELECTOR, ".menu-list a[href='/webtables']")
    BUTTONS_MENU_ITEM = (By.CSS_SELECTOR, ".menu-list a[href='/buttons']")
    LINKS_MENU_ITEM = (By.CSS_SELECTOR, ".menu-list a[href='/links']")

    @property
    def heading(self) -> str:
        return self.find_visible(self.HEADING).text

    def go_to_text_box(self) -> None:
        self.click(self.TEXT_BOX_MENU_ITEM)

    def go_to_check_box(self) -> None:
        self.click(self.CHECK_BOX_MENU_ITEM)

    def go_to_radio_button(self) -> None:
        self.click(self.RADIO_BUTTON_MENU_ITEM)

    def go_to_web_tables(self) -> None:
        self.click(self.WEB_TABLES_MENU_ITEM)

    def go_to_buttons(self) -> None:
        self.click(self.BUTTONS_MENU_ITEM)

    def go_to_links(self) -> None:
        self.click(self.LINKS_MENU_ITEM)
