from selenium.webdriver.common.by import By

from pages.base_page import Locator
from pages.elements_page import ElementsPage


class CheckBoxPage(ElementsPage):
    PATH = "/checkbox"

    FOLDERS = (
        "Home",
        "Desktop",
        "Documents",
        "WorkSpace",
        "Office",
        "Downloads",
    )

    NODE_TITLES = (By.CSS_SELECTOR, ".rc-tree-list .rc-tree-title")
    CHECKED_BOXES = (
        By.CSS_SELECTOR,
        ".rc-tree-list .rc-tree-checkbox[aria-checked='true']",
    )
    RESULT_ITEMS = (By.CSS_SELECTOR, "#result .text-success")

    @staticmethod
    def _checkbox(name: str) -> Locator:
        return (
            By.CSS_SELECTOR,
            f".rc-tree-checkbox[aria-label='Select {name}']",
        )

    @staticmethod
    def _node(name: str) -> Locator:
        return (
            By.CSS_SELECTOR,
            f"[role='treeitem']:has([aria-label='Select {name}'])",
        )

    def _switcher(self, name: str) -> Locator:
        return (By.CSS_SELECTOR, f"{self._node(name)[1]} .rc-tree-switcher")

    def is_expanded(self, name: str) -> bool:
        node = self.find_visible(self._node(name))
        return node.get_attribute("aria-expanded") == "true"

    def _set_expanded(self, name: str, expanded: bool) -> None:
        if self.is_expanded(name) != expanded:
            self.click(self._switcher(name))
            self.wait_until(lambda _: self.is_expanded(name) == expanded)

    def expand(self, name: str) -> None:
        self._set_expanded(name, True)

    def collapse(self, name: str) -> None:
        self._set_expanded(name, False)

    def expand_all(self) -> None:
        for folder in self.FOLDERS:
            self.expand(folder)

    def visible_nodes(self) -> list[str]:
        return [
            title.text for title in self.find_all_visible(self.NODE_TITLES)
        ]

    def toggle(self, name: str) -> None:
        """Click a node's checkbox, which checks or unchecks it."""
        self.click(self._checkbox(name))

    def checkbox_state(self, name: str) -> str:
        """Return 'true', 'false' or, for a partly checked folder, 'mixed'."""
        checkbox = self.find_visible(self._checkbox(name))
        return checkbox.get_attribute("aria-checked")

    def checked_count(self) -> int:
        """Return how many visible nodes are fully checked."""
        return len(self.driver.find_elements(*self.CHECKED_BOXES))

    def selected_items(self) -> set[str]:
        """Return the names shown in the result right now."""
        items = self.driver.find_elements(*self.RESULT_ITEMS)
        return {item.text for item in items}

    def wait_for_selected_items(self) -> set[str]:
        """Wait for a result to appear, then return its names."""
        self.find_all_visible(self.RESULT_ITEMS)
        return self.selected_items()

    def wait_for_selected_items_to_be(self, expected: set[str]) -> set[str]:
        """Wait for an existing result to change, then return its names."""
        self.wait_until(lambda _: self.selected_items() == expected)
        return self.selected_items()
