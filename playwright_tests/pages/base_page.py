from playwright.sync_api import Locator, Page, Response


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

    def reload(self) -> None:
        self.page.reload()

    def file_status(self, path: str) -> int:
        """Request a file from the site directly and return its status code."""
        return self.page.request.get(f"{self.BASE_URL}{path}").status

    @property
    def tab_count(self) -> int:
        return len(self.page.context.pages)

    def click_and_get_page_status(self, link: Locator) -> int:
        """Click a link and return the status code of the page it opens.

        Redirects are skipped, so this is the status of the final page.
        """

        def is_final_page_response(response: Response) -> bool:
            request = response.request
            return (
                request.is_navigation_request()
                and request.frame == self.page.main_frame
                and not 300 <= response.status < 400
            )

        with self.page.expect_response(is_final_page_response) as response:
            link.click()
        return response.value.status
