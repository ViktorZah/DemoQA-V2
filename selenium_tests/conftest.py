import base64
import re

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")

    chrome = webdriver.Chrome(options=options)
    yield chrome
    chrome.quit()


@pytest.fixture
def open_page(driver):
    """Return a function that opens a given page class and returns the page."""

    def _open(page_class):
        page = page_class(driver)
        page.open()
        return page

    return _open


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot of each failed test and add it to the HTML report."""
    outcome = yield
    report = outcome.get_result()

    browser = item.funcargs.get("driver")
    if browser is None or report.when == "teardown" or not report.failed:
        return

    try:
        screenshot = browser.get_screenshot_as_base64()
    except WebDriverException:
        # A dead browser must not replace the test's real failure.
        return

    folder = item.config.rootpath / "reports" / "screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    file_name = re.sub(r"[^\w.-]+", "_", report.nodeid) + ".png"
    (folder / file_name).write_bytes(base64.b64decode(screenshot))

    report.extras = [*getattr(report, "extras", []), extras.png(screenshot)]
