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

## Disabled Radio Button label looks the same as enabled ones

| | |
|---|---|
| **Severity** | Low |
| **Type** | Usability |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/radio-button` |
| **Test** | None |

### Steps to reproduce

1. Open `https://demoqa.com/radio-button`.
2. Compare the `No` label with the `Yes` label, in the browser's developer tools.

### Expected

A disabled option's label looks different, so users can tell it is unavailable.

### Actual

Both labels have the same text color, `rgb(33, 37, 41)`, even though `No` has a
`disabled` class. The radio circle itself was not compared.

### Impact

- **Users:** the label gives no sign that `No` cannot be selected.
- **Automated tests:** none.

## Web Tables age and salary inputs silently cut off typing

| | |
|---|---|
| **Severity** | Low |
| **Type** | Usability |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/webtables` |
| **Test** | None |

### Steps to reproduce

1. Open `https://demoqa.com/webtables` and click Add.
2. Fill in the form, typing `150` as the age.
3. Submit.

### Expected

The form says the value is too long, or allows ages of 100 and over.

### Actual

The field keeps only `15`, and the record is saved with age 15 and no warning.
A salary of `12345678901` is saved as `1234567890`, and names and departments
stop at 25 characters.

### Impact

- **Users:** a record can be saved with a different value from the one typed.

## Web Tables accepts an age of 0

| | |
|---|---|
| **Severity** | Low |
| **Type** | Validation |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/webtables` |
| **Test** | None, the allowed range is not documented |

### Steps to reproduce

1. Open `https://demoqa.com/webtables` and click Add.
2. Fill in the form with `0` as the age, and submit.

### Expected

An age of 0 is rejected.

### Actual

The record is saved with age 0.

### Impact

- **Users:** an unrealistic age can be saved.

## Web Tables add form keeps text after being closed

| | |
|---|---|
| **Severity** | Low |
| **Type** | Usability |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/webtables` |
| **Test** | None, the intended behaviour is not documented |

### Steps to reproduce

1. Open `https://demoqa.com/webtables` and click Add.
2. Type `Jane` as the first name, then close the form with its X.
3. Click Add again.

### Expected

Closing without saving discards what was typed.

### Actual

The first name still contains `Jane`.

### Impact

- **Users:** old text can end up in a new record.

## Web Tables reuses a record ID after a delete

| | |
|---|---|
| **Severity** | Low |
| **Type** | Technical (invalid HTML) |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/webtables` |
| **Test** | None |

### Steps to reproduce

1. Open `https://demoqa.com/webtables`.
2. Delete Alden, the record with `delete-record-2`.
3. Add a new record.

### Expected

The new record gets an unused ID.

### Actual

The new record and Kierra both use `delete-record-3`.

### Impact

- **Users:** none seen separately from the delete bug, which has `xfail` tests.
- **Automated tests:** locating that delete button by ID may find the wrong row.

## Web Tables search with no match gives no message

| | |
|---|---|
| **Severity** | Low |
| **Type** | Usability |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/webtables` |
| **Test** | None |

### Steps to reproduce

1. Open `https://demoqa.com/webtables`.
2. Search for `zzz`.

### Expected

A message says no records were found, and the page count stays sensible.

### Actual

The table is empty with no message, and the page count reads `1 of 0`.

### Impact

- **Users:** an empty table may look like a loading problem.

## Double Click Me and Right Click Me do not respond to Enter

| | |
|---|---|
| **Severity** | Low |
| **Type** | Accessibility |
| **Found on** | 2026-11-05, Chrome 156 |
| **Pages checked** | `/buttons` |
| **Test** | None, the intended behaviour is not documented |

### Steps to reproduce

1. Open `https://demoqa.com/buttons`.
2. Press Enter on `Double Click Me`, then on `Right Click Me`.

### Expected

Keyboard users have some way to trigger each button.

### Actual

Neither shows a message, while `Click Me` responds to Enter and Space. Space and
the keyboard's menu key were not tried on these two buttons.

### Impact

- **Users:** someone using only a keyboard may be unable to get these messages.

## Links API links throw an error in the console on every click

| | |
|---|---|
| **Severity** | Low |
| **Type** | Technical (JavaScript error), no effect on users seen |
| **Found on** | 2026-11-07, Chrome 156 |
| **Pages checked** | `/links` |
| **Test** | None, console errors are not checked by the tests |

### Steps to reproduce

1. Open `https://demoqa.com/links`.
2. Open the browser console.
3. Click any link under "Following links will send an api call", such as
   `Created`.

### Expected

The click sends its request and shows the response, with no errors.

### Actual

The request is sent and the response message appears, but each click also logs
`Uncaught Error: React has blocked a javascript: URL as a security
precaution.` All seven links do this. Their `href` is
`javascript:throw new Error(...)`: React replaced the original `javascript:`
link, so the browser runs it and throws when the link is followed.

### Impact

- **Users:** none seen. The response message still appears.
- **Developers:** the error hides real errors in the console.
- **Not tested:** opening these links in a new tab (middle click or
  Ctrl+click), or what screen readers announce for them.
  They act as buttons but are links.

## Broken Links images have no alt text

| | |
|---|---|
| **Severity** | Low |
| **Type** | Accessibility |
| **Found on** | 2026-11-07, Chrome 156 |
| **Pages checked** | `/broken` |
| **Test** | None |

### Steps to reproduce

1. Open `https://demoqa.com/broken`.
2. Inspect the two `img` elements under "Valid image" and "Broken image".

### Expected

Each image has an `alt` attribute describing it, or `alt=""` if it is only
decoration.

### Actual

Neither image has an `alt` attribute.

### Impact

- **Users:** screen readers may read out the file name or just "image". Not
  tested with a screen reader.
- **Automated tests:** the images have no accessible name, so role-based
  locators cannot tell them apart.

### Workaround for tests

Locate the images by their `src`, such as `img[src='/images/Toolsqa.jpg']`.

## Broken Links valid link uses http and is redirected

| | |
|---|---|
| **Severity** | Low |
| **Type** | Technical (needless redirect) |
| **Found on** | 2026-11-07, Chrome 156 |
| **Pages checked** | `/broken` |
| **Test** | None, the passing test follows the redirect |

### Steps to reproduce

1. Open `https://demoqa.com/broken`.
2. Click "Click Here for Valid Link".

### Expected

The link points straight to `https://demoqa.com/`.

### Actual

It points to `http://demoqa.com`, which answers `301 Moved Permanently` and
redirects to `https://demoqa.com/`, adding an extra request.

### Impact

- **Users:** none seen. The home page opens normally.
