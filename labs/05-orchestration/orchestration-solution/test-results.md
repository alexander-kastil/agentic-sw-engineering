# Test Results

Environment: Windows 11, Node v24.15.0, `jsdom` resolvable from the global install. No dependency was added to this repository. Both harnesses live outside the repo, in the session scratchpad, and load the solution files by absolute path.

## Contract check

The lab's "Read the trace like a reviewer" section states the shared contract. Every item matches the checked-in files.

| Contract item | Where | Result |
|---------------|-------|--------|
| Element id `celsius-input` | `index.html` line 16 | Pass |
| Element id `fahrenheit-input` | `index.html` line 20 | Pass |
| Element id `message` | `index.html` line 23 | Pass |
| Function `celsiusToFahrenheit` | `converter.js` line 1 | Pass |
| Function `fahrenheitToCelsius` | `converter.js` line 5 | Pass |
| Script order `converter.js` then `app.js` | `index.html` lines 25 and 26 | Pass |
| Five files on disk | this folder | Pass |
| File ownership split with no overlap | Coder: `converter.js`, `app.js`, `readme.md`. Frontend: `index.html`, `styles.css` | Pass |

## Harness 1: the conversion functions

`converter.js` declares two plain function statements with no `module.exports`, so `require()` returns an empty object. It is loaded into a `vm` context instead, which runs the file exactly as a browser `<script>` would and exposes both globals.

Command:

```powershell
node C:\Users\ALEXAN~1\AppData\Local\Temp\claude\D--git-classes-agentic-sw-engineering\0b9ef576-0f1b-414a-9114-61b2d233e6e4\scratchpad\test-converter.js
```

Output:

```text
PASS celsiusToFahrenheit(0) = 32 (expected 32)
PASS celsiusToFahrenheit(100) = 212 (expected 212)
PASS celsiusToFahrenheit(-40) = -40 (expected -40)
PASS celsiusToFahrenheit(37) = 98.6 (expected 98.6)
PASS fahrenheitToCelsius(32) = 0 (expected 0)
PASS fahrenheitToCelsius(212) = 100 (expected 100)
PASS fahrenheitToCelsius(-40) = -40 (expected -40)
PASS fahrenheitToCelsius(98.6) = 37 (expected 37)
typeof celsiusToFahrenheit = function
typeof fahrenheitToCelsius = function
ALL CONVERTER TESTS PASSED
```

Per pair:

| Pair | Celsius to Fahrenheit | Fahrenheit to Celsius |
|------|-----------------------|-----------------------|
| 0 C / 32 F | Pass | Pass |
| 100 C / 212 F | Pass | Pass |
| -40 C / -40 F | Pass | Pass |
| 37 C / 98.6 F | Pass | Pass |

## Harness 2: the page

`index.html` is loaded in `jsdom`, then `converter.js` and `app.js` are evaluated in that window in the order the page declares them. Typing is simulated by setting `input.value` and dispatching an `input` event, which is the event `app.js` listens for.

Command:

```powershell
node C:\Users\ALEXAN~1\AppData\Local\Temp\claude\D--git-classes-agentic-sw-engineering\0b9ef576-0f1b-414a-9114-61b2d233e6e4\scratchpad\test-page.js
```

Output:

```text
-- script order in index.html --
converter.js then app.js
-- C to F --
PASS type 0 in celsius-input -> fahrenheit-input: got "32.0", expected "32.0"
PASS type 100 in celsius-input -> fahrenheit-input: got "212.0", expected "212.0"
PASS type -40 in celsius-input -> fahrenheit-input: got "-40.0", expected "-40.0"
PASS type 37 in celsius-input -> fahrenheit-input: got "98.6", expected "98.6"
-- F to C --
PASS type 32 in fahrenheit-input -> celsius-input: got "0.0", expected "0.0"
PASS type 212 in fahrenheit-input -> celsius-input: got "100.0", expected "100.0"
PASS type -40 in fahrenheit-input -> celsius-input: got "-40.0", expected "-40.0"
PASS type 98.6 in fahrenheit-input -> celsius-input: got "37.0", expected "37.0"
-- invalid input --
PASS message text after typing abc: got "Enter a valid number", expected "Enter a valid number"
PASS message visible after typing abc: got false, expected false
PASS fahrenheit-input NOT cleared by abc: got "77.0", expected "77.0"
-- clearing a field --
PASS clearing celsius clears fahrenheit: got "", expected ""
PASS message hidden after clear: got true, expected true
-- message hidden again after a valid entry --
PASS message hidden after valid entry: got true, expected true
PASS fahrenheit after 10: got "50.0", expected "50.0"
ALL PAGE TESTS PASSED
```

Per behaviour:

| Behaviour the lab states | Result |
|--------------------------|--------|
| Typing in `celsius-input` updates `fahrenheit-input` | Pass |
| Typing in `fahrenheit-input` updates `celsius-input` | Pass |
| Negative values work in both directions | Pass, -40 C and -40 F |
| `abc` shows "Enter a valid number" | Pass |
| `abc` does not clear the other field | Pass, the field kept `77.0` from the preceding valid entry |
| Clearing a field clears the other and hides the message | Pass |
| A valid entry after an invalid one hides the message | Pass |

## Note on display formatting

`app.js` writes results with `toFixed(1)`, so the page shows `32.0` where the lab's verification table lists `32`. The values are correct; only the rendering carries a trailing zero. The lab guide and this folder's readme now say so, so a reader checking the table does not read it as a failure.

## Result

24 of 24 assertions pass. No defect was found in `converter.js`, `app.js`, `index.html` or `styles.css`, and no code file was changed.
