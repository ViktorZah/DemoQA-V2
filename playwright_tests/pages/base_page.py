from playwright.sync_api import Page


class BasePage:
    """Actions shared by every page.

    Child classes set PATH and expose their parts as locators. Tests check
    those locators with expect(), which waits and retries by itself.
    """

    BASE_URL = "https://demoqa.com"
    PATH = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.BASE_URL}{self.PATH}"

    def open(self) -> None:
        self.page.goto(self.url)
