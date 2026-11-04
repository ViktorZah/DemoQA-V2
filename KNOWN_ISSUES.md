# Known Issues

Site issues that are logged here but have no automated test.
Issues with a test are marked `xfail` in the `tests/` folder.

## Sidebar menu items reuse the same IDs

| | |
|---|---|
| **Severity** | Low |
| **Type** | Technical (invalid HTML), no effect on users seen |
| **Found on** | 2026-11-04, Chrome 155 |
| **Pages checked** | `/elements`, `/forms` |
| **Test** | None, logged as a note by decision |

### Steps to reproduce

1. Open `https://demoqa.com/forms`.
2. In the browser console, run `document.querySelectorAll('#item-0').length`.

### Expected

Each ID appears once on the page.

### Actual

`item-0` appears 6 times. Nine sidebar IDs are duplicated in total: `item-0` to
`item-8`. Collapsed sidebar sections are hidden but stay in the page's HTML.

### Impact

- **Users:** none seen. Only one copy of each item is visible at a time, and
  the sidebar works normally.
- **Automated tests:** on `/forms`, `By.ID, "item-0"` returns the hidden
  Text Box item, not the visible Practice Form item.
- **Accessibility tools:** not tested.

### Workaround for tests

Do not locate sidebar items by ID. Use the link's destination instead, for
example `.menu-list a[href='/text-box']`.
