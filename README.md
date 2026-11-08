# DemoQA end-to-end tests

End-to-end UI tests for [DemoQA](https://demoqa.com), a public practice site,
written in Python with pytest and the Page Object Model. The project has two
suites, one in Selenium and one in Playwright, to show both tools on the same
kind of work.

| Suite | Folder | Covers |
|---|---|---|
| Selenium 4 | `selenium_tests/` | Home page, Elements from Text Box to Links |
| Playwright | `playwright_tests/` | Home page, Elements from Broken Links on, Forms, Alerts, Frame & Windows, Widgets, Interactions |

The Selenium suite is kept working but no longer extended; every section from
Broken Links onwards is written in Playwright. The Book Store Application
section is not covered.

## Setup

Requires Python 3.14 and Google Chrome (for the Selenium suite).

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
```

Selenium downloads a matching ChromeDriver by itself. The Playwright suite uses
Playwright's own Chromium, installed by the last command.

## Running the tests

A browser window opens by default, so you can watch the tests. Add
`--headless` to run without one.

```bash
.venv/bin/python -m pytest                     # both suites
.venv/bin/python -m pytest playwright_tests    # one suite
.venv/bin/python -m pytest playwright_tests/tests/widgets   # one section
.venv/bin/python -m pytest playwright_tests/tests/widgets/test_slider.py
.venv/bin/python -m pytest -m smoke            # quick checks of the main paths
.venv/bin/python -m pytest --headless          # no browser window
.venv/bin/python -m pytest -n 4 --headless     # in parallel (pytest-xdist)
```

Every test is marked `regression`; a few per page are also marked `smoke`.

After a run, an HTML report is saved to `reports/report.html`. Failed Selenium
tests save a screenshot; failed Playwright tests save a screenshot and a trace
in `reports/playwright/`, which can be opened with:

```bash
.venv/bin/playwright show-trace reports/playwright/<test>/trace.zip
```

## Known site bugs: `xfail` tests and KNOWN_ISSUES.md

DemoQA has many real bugs, such as typos, validation gaps and broken
behaviour. They are recorded in two ways:

- **`xfail` tests.** A bug with a clear correct behaviour gets a test that
  asserts the correct behaviour and is marked
  `xfail(strict=True, raises=AssertionError, reason=...)`. These show as
  "xfailed" in a normal run; that is expected, not a failure. If the site
  fixes the bug, the test passes and strict mode turns that into a failure,
  so the mark can be removed. Known bugs are grouped in `Test...KnownBugs`
  classes, one bug per test.
- **[`KNOWN_ISSUES.md`](KNOWN_ISSUES.md).** Issues logged without a test,
  mostly accessibility gaps and invisible technical problems, written as bug
  reports: severity, steps to reproduce, expected, actual and impact.

Passing tests never depend on a known bug. Where a name the tests navigate by
is misspelled on the site (for example "Accordian"), they accept either
spelling, and only the `xfail` asks for the correct one.

To see a known bug fail for real:

```bash
.venv/bin/python -m pytest --runxfail -k "<test name>" --headless
```

## Project layout

```
selenium_tests/
  pages/       page classes (locators and actions, no assertions)
  tests/       tests (assertions, no locators)
  conftest.py  driver and failure screenshots
playwright_tests/
  pages/       page classes exposing Playwright Locators
    base_page.py, section_page.py, home_page.py, calendar.py
    elements/  forms/  alerts_windows/  widgets/  interactions/
  tests/       tests, asserting with expect(), in the same section folders
  conftest.py  Playwright's Chromium, window size, open_page fixture
conftest.py    the shared --headless option
pytest.ini     markers, report and trace settings
```

The Playwright pages and tests are grouped by the site's sidebar sections,
so a whole section can be run by its folder. The Selenium suite covers one
section and stays flat.

The folders are not named `selenium/` and `playwright/`, because Python would
import them instead of the real packages.

## Design notes

- **No fixed sleeps.** Selenium uses explicit waits only. Playwright tests
  assert with `expect()`, which retries by itself.
- **Two condition waits in the Playwright suite**, each documented in the code
  with its cause:
  - The site's header logo loads without a set size, just after the page,
    and pushes the content down 76px. Pages that hover or drag wait for it
    first (`BasePage.wait_for_header_to_settle`).
  - The drag library on Droppable and Dragabble sets itself up only when the
    mouse first reaches a draggable box, and ignores a drag begun before
    then. Drags wait for it (`InteractionsPage`).
- **Controlled time.** The Progress Bar tests use Playwright's clock to jump
  the page's timers forward, instead of waiting 10 real seconds.
- **Independent tests.** Selenium starts a new browser per test; Playwright
  gives each test a new browser context.

## Notes

The tests run against the live public site, which shows ads and changes from
time to time. A run can fail for reasons outside the tests, such as a slow
load, an ad covering an element or a network change; check the report or
trace before assuming a test is broken. If the site answers a Playwright
test's page request with an error, such as a 502 during an outage, the
test stops at once with a `PageLoadError` naming the status.
