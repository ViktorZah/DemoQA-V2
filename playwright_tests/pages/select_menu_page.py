from playwright.sync_api import Locator

from playwright_tests.pages.widgets_page import WidgetsPage


class SelectMenuPage(WidgetsPage):
    """Three react-select fields and two native selects.

    None of the fields is tied to its label, so they are found by ID. The
    react-select parts have generated class names such as
    "css-1dimb5e-singleValue"; only the ending is react-select's own, so
    they are matched by that ending.
    """

    PATH = "/select-menu"

    # The single-choice react-select fields, by their label on the page.
    SINGLE_FIELDS = {
        "Select Value": "#withOptGroup",
        "Select One": "#selectOne",
    }
    # The multiselect's box has no ID; its input's ID is generated in page
    # order, so it stays the same on every load.
    MULTI_INPUT = "#react-select-4-input"

    def _single_field(self, label: str) -> Locator:
        return self.page.locator(self.SINGLE_FIELDS[label])

    @property
    def _multi_field(self) -> Locator:
        return self.page.locator(".css-b62m3t-container").filter(
            has=self.page.locator(self.MULTI_INPUT)
        )

    @property
    def _open_list(self) -> Locator:
        # The react-select list; the native multi select is a listbox too.
        return self.page.locator("[id$='-listbox']")

    @property
    def options(self) -> Locator:
        return self._open_list.get_by_role("option")

    @property
    def group_headings(self) -> Locator:
        return self._open_list.locator("[id$='-heading']")

    def placeholder(self, label: str) -> Locator:
        return self._single_field(label).locator("[class*='placeholder']")

    def chosen(self, label: str) -> Locator:
        return self._single_field(label).locator("[class*='singleValue']")

    def open_options(self, label: str) -> None:
        self._single_field(label).click()

    def choose(self, label: str, option: str) -> None:
        self.open_options(label)
        self._option(option).click()

    def _option(self, name: str) -> Locator:
        return self._open_list.get_by_role("option", name=name, exact=True)

    @property
    def multi_placeholder(self) -> Locator:
        return self._multi_field.locator("[class*='placeholder']")

    @property
    def chosen_colours(self) -> Locator:
        return self._multi_field.locator(
            "[class*='multiValue'] > div:first-child"
        )

    def open_multi_options(self) -> None:
        self.page.locator(self.MULTI_INPUT).click()

    def choose_colours(self, *colours: str) -> None:
        """Choose colours one after another; the list stays open."""
        self.open_multi_options()
        for colour in colours:
            self._option(colour).click()
        self.page.keyboard.press("Escape")

    def remove_colour(self, colour: str) -> None:
        self.page.get_by_role("button", name=f"Remove {colour}").click()

    def press_in_multi_field(self, key: str) -> None:
        self.page.locator(self.MULTI_INPUT).press(key)

    @property
    def old_select(self) -> Locator:
        return self.page.locator("#oldSelectMenu")

    @property
    def old_select_options(self) -> Locator:
        return self.old_select.locator("option")

    @property
    def old_select_chosen(self) -> Locator:
        return self.old_select.locator("option:checked")

    def choose_old_select(self, colour: str) -> None:
        self.old_select.select_option(label=colour)

    @property
    def cars(self) -> Locator:
        return self.page.locator("#cars")

    @property
    def car_options(self) -> Locator:
        return self.cars.locator("option")

    def choose_cars(self, *cars: str) -> None:
        self.cars.select_option(label=list(cars))
