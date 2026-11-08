from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
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
    # True once every image in the header has finished, loaded or failed.
    HEADER_IMAGES_DONE = """
        return [...document.querySelectorAll('header img')]
            .every(image => image.complete);
    """
    # Collects for half a second, as the browser reports shifts a moment later.
    LAYOUT_SHIFT_SCORE = """
        const done = arguments[0];
        let score = 0;
        new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) score += entry.value;
        }).observe({type: 'layout-shift', buffered: true});
        setTimeout(() => done(score), 500);
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self) -> None:
        self.driver.get(f"{self.BASE_URL}{self.PATH}")

    def reload(self) -> None:
        self.driver.refresh()

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

    @property
    def tab_count(self) -> int:
        return len(self.driver.window_handles)

    def wait_for_tab_count(self, count: int) -> bool:
        return self.wait_until(EC.number_of_windows_to_be(count))

    def switch_to_newest_tab(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all_visible(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def _find_clickable_in_view(self, locator: Locator) -> WebElement:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # Centre the element so fixed page elements cannot cover it.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return element

    def click(self, locator: Locator) -> None:
        self._find_clickable_in_view(locator).click()

    def _wait_for_header_to_settle(self) -> None:
        """Wait for the header's logo, which pushes the content down.

        The logo has no set size and arrives just after the page loads, so
        the header grows from 24px to 100px and the content moves down
        76px. ActionChains clicks a position on screen, so a click sent
        before that would miss its element.

        Raises TimeoutException if the logo never finishes. An earlier
        check here could never come true after a site change, and because
        its timeout was ignored, every call quietly waited 10 seconds.
        """
        self.wait.until(
            lambda driver: driver.execute_script(self.HEADER_IMAGES_DONE)
        )

    def layout_shift_score(self) -> float:
        """Return how much the content has moved since the page loaded.

        This is the browser's own measure, and 0 means nothing moved.
        """
        self._wait_for_header_to_settle()
        return self.driver.execute_async_script(self.LAYOUT_SHIFT_SCORE)

    def double_click(self, locator: Locator) -> None:
        self._wait_for_header_to_settle()
        element = self._find_clickable_in_view(locator)
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, locator: Locator) -> None:
        self._wait_for_header_to_settle()
        element = self._find_clickable_in_view(locator)
        ActionChains(self.driver).context_click(element).perform()

    def type_text(self, locator: Locator, text: str) -> None:
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)
