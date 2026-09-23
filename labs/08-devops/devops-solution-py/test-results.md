# Lab 08 devops test results (Python)

All commands ran with Python 3.12.10 and pytest 9.0.3 on Windows, from this folder unless stated otherwise. Every command below is verbatim, followed by the real output.

## Tests against the fixed app

```bash
python -m pytest
```

```text
tests\test_security_fixes.py ........                                    [100%]

============================== 8 passed in 2.12s ==============================
```

## Tests against the unfixed starter

The same `tests/` folder copied into a scratch copy of `contososhopeasy-py/`:

```bash
python -m pytest
```

```text
========================= 7 failed, 1 passed in 2.20s =========================
```

The one test that passes on the starter is `test_search_products_sanitizes_malicious_input`: the in-memory repository already returns no products for the injection string, which is why the issue is about the logged query, not the result set.

## Run

```bash
python -m contoso_shop_easy
```

Lines that changed against the starter run:

```text
Credit card storage: LAST 4 DIGITS ONLY, NO CVV (SECURE)
SQL injection protection: ENABLED (search input sanitized)
Searching for: 'laptop'
Found 2 products
[DEBUG] Validating credit card ending in 0366
[DEBUG] Processing payment for card ending in 0366
[LOG] Payment completed - Card: ****0366, Amount: $2949.98, Transaction: TXN_202609231606_0366_294998
Total products in catalog: 40
Total registered users: 8
Total revenue: $6381.89
```

No `[DEBUG] SQL Query:` line, no full card number and no `CVV:` line appear anywhere in the output. The closing totals match the starter run.

## Guide walk-through

The guide's local steps ran in a scratch `ResolveGitHubIssues` folder: `Copy-Item -Recurse` of the starter (the hidden `.github` folder is copied), `git init -b main`, first commit, the first run, the SQL fix and a run, the `PaymentInfo` change alone (the run stops with `TypeError: PaymentInfo.__init__() got an unexpected keyword argument 'card_number'`), the remaining fixes, the `Select-String` check (prints nothing), and the final commit. `git status` stayed free of `__pycache__` throughout. The workflow's ten `github-script` steps were executed under Node against a stubbed `github.rest.issues.create` and produced the ten expected titles and labels.

Not executed: the push to GitHub, the Actions run on github.com, the GitHub Pull Requests extension, and the Copilot Ask and Agent mode steps.
