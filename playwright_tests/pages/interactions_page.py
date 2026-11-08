from playwright.sync_api import Locator

from playwright_tests.pages.section_page import SectionPage


class InteractionsPage(SectionPage):
    # The section's own page has no heading.
    PATH = "/interaction"

    # How far left of an element the mouse starts before gliding onto it.
    GLIDE_FROM_PX = 150

    def open(self) -> None:
        """Open the page and wait until the content has stopped moving.

        Every Interactions page is about dragging or clicking positions,
        which need a still page; see wait_for_header_to_settle.
        """
        super().open()
        self.wait_for_header_to_settle()

    def go_to_sortable(self) -> None:
        self._menu_item("Sortable").click()

    def go_to_selectable(self) -> None:
        self._menu_item("Selectable").click()

    def go_to_resizable(self) -> None:
        self._menu_item("Resizable").click()

    def go_to_droppable(self) -> None:
        self._menu_item("Droppable").click()

    @staticmethod
    def _centre(element: Locator) -> tuple[float, float]:
        box = element.bounding_box()
        return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2

    def _wait_until_draggable(self, element: Locator) -> None:
        """Wait for the page's drag library to take hold of the element.

        The library is set up lazily: about 0.2s after the mouse first
        reaches a draggable element, every draggable gets the class
        "ui-draggable". A drag begun before then does nothing. This is the
        second wait in the Playwright suite, chosen by the user on
        2026-11-08; it waits for that class, never for a fixed time.
        """
        element.and_(self.page.locator(".ui-draggable")).wait_for()

    def _pick_up(self, source: Locator) -> tuple[float, float]:
        """Press on source's centre, ready to drag; return that point.

        The mouse glides onto source the way a person's would and waits
        for the drag library before pressing.
        """
        x, y = self._centre(source)
        self.page.mouse.move(x - self.GLIDE_FROM_PX, y)
        self.page.mouse.move(x, y, steps=10)
        self._wait_until_draggable(source)
        self.page.mouse.down()
        return x, y

    def hold_over(
        self,
        source: Locator,
        target: Locator,
        offset: tuple[float, float] | None = None,
    ) -> None:
        """Pick up source and hold it over target, without dropping it.

        The mouse moves in steps to target's centre, or to offset (x, y)
        from target's top-left corner.
        """
        self._pick_up(source)
        if offset is None:
            to_x, to_y = self._centre(target)
        else:
            box = target.bounding_box()
            to_x, to_y = box["x"] + offset[0], box["y"] + offset[1]
        self.page.mouse.move(to_x, to_y, steps=15)

    def release(self) -> None:
        self.page.mouse.up()

    def drag_onto(
        self,
        source: Locator,
        target: Locator,
        offset: tuple[float, float] | None = None,
    ) -> None:
        self.hold_over(source, target, offset)
        self.release()
