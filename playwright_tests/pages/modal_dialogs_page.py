from playwright.sync_api import Locator

from playwright_tests.pages.alerts_windows_page import AlertsWindowsPage


class ModalDialogsPage(AlertsWindowsPage):
    PATH = "/modal-dialogs"

    # Each size's button and dialog title.
    MODALS = {
        "small": ("Small modal", "Small Modal"),
        "large": ("Large modal", "Large Modal"),
    }

    @property
    def intro(self) -> Locator:
        return self.page.get_by_text(
            "Click on button to see modal", exact=True
        )

    def open_button(self, size: str) -> Locator:
        name = self.MODALS[size][0]
        return self.page.get_by_role("button", name=name, exact=True)

    def dialog(self, size: str) -> Locator:
        title = self.MODALS[size][1]
        return self.page.get_by_role("dialog", name=title, exact=True)

    @property
    def any_dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    def body(self, size: str) -> Locator:
        return self.dialog(size).locator(".modal-body")

    def open_modal(self, size: str) -> None:
        self.open_button(size).click()
        self.dialog(size).wait_for()

    def dialog_width(self, size: str) -> float:
        return self.size_of(self.dialog(size).locator(".modal-content"))[0]

    def close(self, size: str, way: str) -> None:
        """Close the dialog: footer button, corner x, Escape or outside."""
        dialog = self.dialog(size)
        # Both the corner x and the footer button are named "Close".
        if way == "footer":
            dialog.locator(".modal-footer").get_by_role(
                "button", name="Close"
            ).click()
        elif way == "x":
            dialog.locator(".modal-header").get_by_role(
                "button", name="Close"
            ).click()
        elif way == "escape":
            self.page.keyboard.press("Escape")
        else:
            # The dialog covers the page with a backdrop, so a point beside
            # the dialog box lands on it.
            self.page.mouse.click(30, 540)
