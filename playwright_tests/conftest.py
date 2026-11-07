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
