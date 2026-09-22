# Lab 05 Solution: Agent Sessions

The artifacts Lab 05 asks you to end up with, in the state they should reach by Step 10. In the lab they live in `src/scratch/session-lab/` and the Cleanup section deletes them; here they are kept so you can compare.

| File | Produced by | What it is |
|------|-------------|------------|
| `research.md` | Step 2 | The cited scoping report from the read-only research session: how `src/` organizes its sample projects and which manifest each project type carries |
| `slugify.js` | Step 3, hardened in Step 8 | The single exported `slugify(input)` the writing session builds in its worktree |
| `slugify.test.js` | Step 3, extended in Step 8 | Nine tests: the ordinary case and the empty string from Step 3, plus the three edge cases Step 8 predicts the reviewer raises |
| `package.json` | Step 7 | The minimal manifest whose absence makes the Step 7 run fail, with a `test` script on `node --test` and no dependencies |
| `handover.md` | Step 10 | The five-section assembly of all four surfaces |
| `test-results.md` | This run | Every command run verbatim, its output, a pass or fail line per test case, and the steps that could not be executed outside the Agents window |

Run the tests with Node 20 or later:

```bash
npm test
```

No install step: the tests use Node's built-in runner and the manifest declares no dependencies.
