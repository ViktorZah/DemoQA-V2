from playwright.sync_api import Locator

from playwright_tests.pages.widgets_page import WidgetsPage


class SliderPage(WidgetsPage):
    PATH = "/slider"

    @property
    def slider(self) -> Locator:
        return self.page.get_by_role("slider")

    @property
    def value_box(self) -> Locator:
        # The box beside the slider has no label, so it is found by ID.
        return self.page.locator("#sliderValue")

    @property
    def tooltip(self) -> Locator:
        return self.page.locator(".range-slider__tooltip__label")

    def press_on_slider(self, key: str) -> None:
        self.slider.press(key)

    def set_value(self, value: int) -> None:
        self.slider.fill(str(value))

    def click_slider_edge(self, edge: str) -> None:
        """Click the left or right end of the slider's track."""
        box = self.slider.bounding_box()
        x = box["x"] + 1 if edge == "left" else box["x"] + box["width"] - 1
        self.page.mouse.click(x, box["y"] + box["height"] / 2)

    def type_in_value_box(self, text: str) -> None:
        self.value_box.click()
        self.value_box.press("ControlOrMeta+a")
        self.value_box.press_sequentially(text)

    def press_enter_in_value_box(self) -> None:
        """Press Enter in the value box, and wait for any page reload."""
        self.value_box.press("Enter")
        self.page.wait_for_load_state()

    def value_box_is_read_only(self) -> bool:
        return self.value_box.evaluate("box => box.readOnly")
