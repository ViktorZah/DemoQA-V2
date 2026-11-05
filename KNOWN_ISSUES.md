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

## Clicking a Check Box label does not check its box

| | |
|---|---|
| **Severity** | Low |
| **Type** | Usability |
| **Found on** | 2026-11-04, Chrome 156 |
| **Pages checked** | `/checkbox` |
| **Test** | None, the intended behaviour is not documented |

### Steps to reproduce

1. Open `https://demoqa.com/checkbox`.
2. Expand Home.
3. Click the word `Desktop`, not its checkbox.

### Expected

Clicking a checkbox's label usually toggles the checkbox.

### Actual

The row is highlighted, but its box stays unchecked and no result appears.

### Impact

- **Users:** someone clicking the label may think they selected the item.
- **Automated tests:** tests must click the checkbox itself.

## Check Box files are announced as collapsible

| | |
|---|---|
| **Severity** | Low |
| **Type** | Technical (accessibility markup) |
| **Found on** | 2026-11-04, Chrome 156 |
| **Pages checked** | `/checkbox` |
| **Test** | None |

### Steps to reproduce

1. Open `https://demoqa.com/checkbox` and expand down to `Notes`.
2. Inspect the `Notes` row, which has `role="treeitem"`.

### Expected

A file has no children, so its row has no `aria-expanded` attribute.

### Actual

The row has `aria-expanded="false"`, which marks it as a collapsed folder.

### Impact

- **Users:** none seen in the browser.
- **Accessibility tools:** not tested, but they may announce it as collapsed.
