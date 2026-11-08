from playwright.sync_api import Locator

from playwright_tests.pages.interactions.interactions_page import (
    InteractionsPage,
)


class ResizablePage(InteractionsPage):
    PATH = "/resizable"

    # The boxes have no role or name, so they are found by ID.
    BOXES = {
        "limited": "#resizableBoxWithRestriction",
        "free": "#resizable",
    }

    def box(self, name: str) -> Locator:
        return self.page.locator(self.BOXES[name])

    def box_text(self, name: str) -> Locator:
        return self.box(name).locator(".text")

    def box_size(self, name: str) -> tuple[float, float]:
        return self.size_of(self.box(name))

    def resize(self, name: str, dx: float, dy: float) -> None:
        """Drag the box's bottom-right handle by dx and dy pixels."""
        handle = self.box(name).locator(".react-resizable-handle")
        box = handle.bounding_box()
        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x + dx, y + dy, steps=10)
        self.page.mouse.up()
