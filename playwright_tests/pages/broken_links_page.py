from playwright.sync_api import Locator

from playwright_tests.pages.elements_page import ElementsPage


class BrokenLinksPage(ElementsPage):
    PATH = "/broken"

    # The images have no alt text, so no accessible name to find them by.
    IMAGES = {
        "valid": "img[src='/images/Toolsqa.jpg']",
        "broken": "img[src='/images/Toolsqa_1.jpg']",
    }
    LINKS = {
        "valid": "Click Here for Valid Link",
        "broken": "Click Here for Broken Link",
    }
    # True once the image has drawn, false once it has failed. Resolves
    # straight away if the browser has already finished with it.
    IMAGE_LOADED = """
        image => image.complete
            ? image.naturalWidth > 0
            : new Promise(resolve => {
                image.addEventListener('load', () => resolve(true));
                image.addEventListener('error', () => resolve(false));
            })
    """

    @property
    def labels(self) -> Locator:
        return self.page.locator("h1 ~ p")

    def link(self, link: str) -> Locator:
        return self.page.get_by_role("link", name=self.LINKS[link], exact=True)

    def image_loaded(self, image: str) -> bool:
        """Wait for the browser to finish with an image, and say if it drew."""
        locator = self.page.locator(self.IMAGES[image])
        return locator.evaluate(self.IMAGE_LOADED)

    def image_file_status(self, image: str) -> int:
        """Return the status code the server gives for an image's file."""
        locator = self.page.locator(self.IMAGES[image])
        return self.file_status(locator.get_attribute("src"))

    def follow_link(self, link: str) -> int:
        """Click a link and return the status code of the page it opens."""
        return self.click_and_get_page_status(self.link(link))
