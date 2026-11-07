import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Show the browser window unless --headless is given.

    The suite uses Playwright's own Chromium, not the installed Chrome. With
    the installed Chrome, the browser twice quit cleanly in the middle of a
    run for no known reason.
    """
    return {
        **browser_type_launch_args,
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
