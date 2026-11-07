import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Use the installed Chrome, with a visible window unless --headless."""
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": pytestconfig.getoption("--headless"),
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture
def open_page(page):
    """Return a function that opens a given page class and returns the page."""

    def _open(page_class):
        page_object = page_class(page)
        page_object.open()
        return page_object

    return _open
