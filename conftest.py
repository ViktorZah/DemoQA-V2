def pytest_addoption(parser):
    """Options shared by the Selenium and Playwright suites."""
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run Chrome without opening a browser window.",
    )
