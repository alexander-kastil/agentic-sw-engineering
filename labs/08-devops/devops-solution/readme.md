# Lab 08 devops solution

Refactored source for the two issues assigned in `labs/08-devops/readme.md`, applied to the ContosoShopEasy console app. Files are full files, laid out under `ContosoShopEasy/` mirroring their real paths in the `resolve-github-issues-lab-project` repository. `ContosoShopEasy.Tests/` is a new xUnit project that proves the fixes hold, since the guide's own testing step (read the console output) does not assert anything.

## Files and the issue each one resolves

- `ContosoShopEasy/Models/Order.cs` - **Fix Credit Card Data Storage Violations**. `PaymentInfo` no longer has `CardNumber` or `CVV`. Replaced with `CardLastFourDigits` and `CardType`.
- `ContosoShopEasy/Services/PaymentService.cs` - **Fix Credit Card Data Storage Violations**. `ProcessPayment` no longer logs the full card number or CVV, stores only the last four digits and detected card type on `PaymentInfo`, and masks the card number in every remaining log line. Added `MaskCardNumber` and `DetectCardType` helpers.
- `ContosoShopEasy/Security/SecurityValidator.cs` - **Fix Credit Card Data Storage Violations** and **Fix SQL Injection Vulnerability in Product Search**. `ValidateCreditCard` masks the card number in its log line instead of printing it in full. `DisplayKnownVulnerabilities` now reports credit card storage as secure and SQL injection protection as enabled.
- `ContosoShopEasy/Services/ProductService.cs` - **Fix SQL Injection Vulnerability in Product Search**. `SearchProducts` no longer builds or logs the simulated SQL query string. Added `SanitizeSearchTerm`, which trims the term, caps it at 100 characters, and strips `' " ; < > -` before the term reaches `ProductRepository`.
- `ContosoShopEasy.Tests/ContosoShopEasy.Tests.csproj`, `ContosoShopEasy.Tests/SecurityFixTests.cs` - new test project (xUnit, net9.0) that captures console output and asserts the vulnerabilities are actually gone.

`Data/OrderRepository.cs` needed no changes: it persists whatever is on `PaymentInfo`, so once `PaymentInfo` stopped carrying the full card number and CVV, the repository stopped persisting them too.

See `test-results.md` for every command run and its output.
