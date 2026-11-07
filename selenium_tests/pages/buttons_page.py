from selenium.webdriver.common.by import By

from selenium_tests.pages.elements_page import ElementsPage


class ButtonsPage(ElementsPage):
    PATH = "/buttons"

    ALL_BUTTONS = (By.CSS_SELECTOR, "h1 ~ div > .btn-primary")
    BUTTONS = {
        "Double Click Me": (By.ID, "doubleClickBtn"),
        "Right Click Me": (By.ID, "rightClickBtn"),
        # This button gets a new random ID on every page load.
        "Click Me": (
            By.CSS_SELECTOR,
            "h1 ~ div > .btn-primary"
            ":not(#doubleClickBtn):not(#rightClickBtn)",
        ),
    }
    MESSAGES = {
        "Double Click Me": (By.ID, "doubleClickMessage"),
        "Right Click Me": (By.ID, "rightClickMessage"),
        "Click Me": (By.ID, "dynamicClickMessage"),
    }

    def button_labels(self) -> list[str]:
        buttons = self.find_all_visible(self.ALL_BUTTONS)
        return [button.text for button in buttons]

    def click_button(self, button: str, kind: str = "left") -> None:
        """Click a button the given way: left, double or right."""
        clicks = {
            "left": self.click,
            "double": self.double_click,
            "right": self.right_click,
        }
        clicks[kind](self.BUTTONS[button])

    def press_key_on_button(self, button: str, key: str) -> None:
        self.find_visible(self.BUTTONS[button]).send_keys(key)

    def messages(self) -> dict[str, str]:
        """Return the messages shown right now, by button."""
        shown = {}
        for button, locator in self.MESSAGES.items():
            elements = self.driver.find_elements(*locator)
            if elements:
                shown[button] = elements[0].text
        return shown

    def wait_for_message(self, button: str) -> str | None:
        """Wait for a button's message to appear, then return it."""
        self.wait_until(lambda _: button in self.messages())
        return self.messages().get(button)
