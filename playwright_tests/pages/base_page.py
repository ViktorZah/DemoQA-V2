from playwright.sync_api import Locator, Page, Response


class BasePage:
    """Actions shared by every page.

    Child classes set PATH and expose their parts as locators. Tests check
    those locators with expect(), which waits and retries by itself.
    """

    BASE_URL = "https://demoqa.com"
    PATH = "/"

    # True once every image in the header has finished, loaded or failed.
    HEADER_IMAGES_DONE = """() => [...document.querySelectorAll('header img')]
        .every(image => image.complete)"""

    def __init__(self, page: Page) -> None:
        self.page = page

    def wait_for_header_to_settle(self) -> None:
        """Wait for the header's logo, which pushes the content down.

        The logo has no set size and arrives just after the page loads, so
        the header grows from 24px to 100px and the content moves down
        76px. A hover sent before that lands where the element used to be.
        expect() cannot help, as it retries checks, not actions. So this is
        the one wait in the Playwright suite, chosen by the user on
        2026-11-08. Use it only for actions that need a still page, such as
        hovering.
        """
        self.page.wait_for_function(self.HEADER_IMAGES_DONE)

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

    @staticmethod
    def size_of(element: Locator) -> tuple[float, float]:
        """Return an element's width and height on the page."""
        box = element.bounding_box()
        return box["width"], box["height"]

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
