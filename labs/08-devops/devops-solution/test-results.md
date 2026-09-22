# Lab 08 devops test results

All commands ran against the scratchpad clone of `resolve-github-issues-lab-project` after the fixes in this folder were applied there (net9.0, dotnet SDK 10.0.112). Every command below is verbatim, followed by the real output tail.

## Build

```bash
cd ContosoShopEasy
dotnet build
```

```text
Determining projects to restore...
All projects are up-to-date for restore.
ContosoShopEasy -> ...\ContosoShopEasy\bin\Debug\net9.0\ContosoShopEasy.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:00.90
```

Also built the whole solution (`dotnet build resolve-github-issues-lab-project.sln`) from the repo root: same result, 0 warnings, 0 errors.

## Run

```bash
dotnet run
```

Exit code: `0`. Relevant lines from the captured output:

```text
Searching for: 'laptop'
Found 2 products
  -> Dell XPS 13 - $1899,99 (Dell)

Searching for: ''; DROP TABLE Products; --'
Found 0 products

Processing payment for Diego Siciliani
[DEBUG] Validating credit card ending in 0366
[DEBUG] Processing payment for card ending in 0366
[LOG] Payment completed - Card: ****0366, Amount: $2949,98, Transaction: TXN_202609211954_0366_2949,98
```

Checks against the full captured output (`grep -c` over the whole run):

- `4532015112830366|5555555555554444|4111111111111111` (the three raw card numbers used in the demo payments): **0 matches**.
- `CVV: 123|CVV: 456|CVV: 789` (the three raw CVVs used in the demo payments): **0 matches**.
- `SQL Query` (case-insensitive, the old simulated-query log line): **0 matches**.

## Automated tests

```bash
cd ContosoShopEasy.Tests
dotnet test
```

```text
Starting test execution, please wait...
A total of 1 test files matched the specified pattern.

Passed!  - Failed:     0, Passed:     5, Skipped:     0, Total:     5, Duration: 1 s - ContosoShopEasy.Tests.dll (net9.0)
```

The five tests in `SecurityFixTests.cs`:

1. `ProcessPayment_DoesNotLogFullCardNumberOrCvv` - runs a real payment, asserts the captured console output contains neither the full card number nor the CVV, and does contain the last four digits.
2. `ValidateCreditCard_DoesNotLogFullCardNumber` - same assertion against `SecurityValidator.ValidateCreditCard`.
3. `SearchProducts_DoesNotLogSimulatedSqlQuery` - asserts the captured output never contains `SELECT * FROM Products` and that a legitimate search still returns results.
4. `SearchProducts_SanitizesMaliciousInputWithoutThrowing` - runs the `'; DROP TABLE Products; --` search term used in `Program.cs` and asserts it does not throw and returns no results.
5. `PaymentInfo_HasNoCardNumberOrCvvProperty` - reflection check that `CardNumber` and `CVV` are gone from `PaymentInfo` and `CardLastFourDigits`/`CardType` exist.

## Pass/fail summary

| Issue / check | Result |
|---|---|
| Fix SQL Injection Vulnerability in Product Search | PASS - simulated query logging removed, malicious input sanitized, legitimate searches still return results |
| Fix Credit Card Data Storage Violations | PASS - `CardNumber`/`CVV` removed from `PaymentInfo`, only last four digits and card type stored, all logs masked |
| `dotnet build` (project and solution) | PASS - 0 warnings, 0 errors |
| `dotnet run` (manual guide step) | PASS - exit code 0, no sensitive data in console output |
| `dotnet test` (added, since the guide's own step is a manual read) | PASS - 5/5 |

## Steps that could not be executed mechanically

- Importing the repository via GitHub Importer and running the "Create ContosoShopEasy Training Issues" workflow: needs a GitHub account and the GitHub UI.
- Reviewing, filtering, and self-assigning the GitHub issues: needs the GitHub Issues UI.
- Every "Ask GitHub Copilot..." step in the Ask-mode analysis sections: needs GitHub Copilot Chat inside VS Code.
- Every "select Keep in the Chat view" step in the Agent-mode remediation sections: needs GitHub Copilot Agent mode inside VS Code; the equivalent code changes were applied directly instead and are described above.
- Drafting a commit message with Copilot Chat, committing, pushing, and verifying the issues auto-close: needs a real GitHub repository and push access, and this session was explicitly told not to create one, push, or open/close issues.
