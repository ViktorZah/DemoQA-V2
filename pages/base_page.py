from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


class BasePage:
    """Actions shared by every page.

    Child classes set PATH and their own locators.
    """

    BASE_URL = "https://demoqa.com"
    PATH = "/"
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self) -> None:
        self.driver.get(f"{self.BASE_URL}{self.PATH}")

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def wait_until(self, condition) -> bool:
        """Return whether the condition came true before the timeout."""
        try:
            self.wait.until(condition)
        except TimeoutException:
            return False
        return True

    def wait_for_url(self, url: str) -> bool:
        return self.wait_until(EC.url_to_be(url))

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all_visible(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: Locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # Centre the element so fixed page elements cannot cover it.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()

    def type_text(self, locator: Locator, text: str) -> None:
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)
