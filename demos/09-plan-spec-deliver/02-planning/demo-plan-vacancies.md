# Plan the Vacancies Feature and File It as Issues

HR wants to track open positions in the HR MCP server, and the fastest way to get that wrong is to let an agent start coding on a one-line request. In this demo Copilot researches the server with three parallel subagents that share one ledger file, writes a plan you can check line by line against that ledger, and files the plan as a GitHub parent issue with one sub-issue per task.

------

Start the Copilot CLI from the repository root. The run writes two files to `demos/09-plan-spec-deliver/02-planning/vacancies-plan/` and creates issues on your GitHub repository; delete the folder and close the issues to reset.

---

## Demo Files

| File | What it represents |
|------|--------------------|
| [src/hr-mcp-server](/src/hr-mcp-server/readme.md) | The server being planned: five employee tools over MCP, SQLite storage |
| [.github/skills/create-issue/SKILL.md](/.github/skills/create-issue/SKILL.md) | The skill behind `/create-issue`: parent issue, sub-issues, labels |
| [vacancies-plan-solution/](./vacancies-plan-solution/) | A verified run: `ledger.md` written by three subagents, `plan.md` written from it |

> Note: If you routed the CLI to your own model provider in [Bring Your Own Key in the Copilot CLI](../../08-governance/02-cost-byok/02-byok-copilot-cli/readme.md), the `COPILOT_PROVIDER_*` variables override `--model` for every call, subagents included. Remove them for this session so the planning runs on a hosted Copilot model.

---

## Step 1: Research in parallel through a shared ledger

**Overview:** Three subagents read the tool layer, the data layer and the verification path at the same time. Subagents are stateless, so the prompt creates the ledger first and names it in every subagent's brief; that file is the only state they share.

Start the CLI in fleet mode so the agent may run subagents in parallel, then paste the prompt:

```powershell
copilot --fleet
```

**Recipe:**

```text
Plan adding vacancies (open positions) to the HR MCP server in src/hr-mcp-server. HR wants to record a vacancy with a title, required skills, required languages and a status of open or filled, list and close vacancies, and find existing employees whose skills match a vacancy.

First create the shared ledger demos/09-plan-spec-deliver/02-planning/vacancies-plan/ledger.md with three empty headings: MCP tools, Data, Verification.

Then use your task tool to run three general-purpose subagents in parallel (not explore agents, which cannot write files). Research only inside src/hr-mcp-server; ignore bin, obj and publish. Tell each subagent the ledger path and to write its findings under its own heading in that file, and nothing else:
1. MCP tools: how Tools/HRTools.cs declares tools, names parameters and returns results.
2. Data: Tools/Models.cs, Data/EmployeeDbContext.cs and Data/EmployeeDbInitializer.cs, and how the SQLite schema is created and seeded.
3. Verification: the smoke test in readme.md and inspector.config.json, and how a new tool would be checked.

When all three are done, read the ledger and write the plan to demos/09-plan-spec-deliver/02-planning/vacancies-plan/plan.md: a one-paragraph summary, then numbered tasks, each with the files it touches, the tasks it depends on, and acceptance criteria. The ledger and the plan are the only files written: do not change any code and do not write tasks/todo.md.
```

**Expected Outcome:** The session reports three `general-purpose` subagents dispatched in parallel, then two files. `ledger.md` has the three headings, each filled by a different subagent with file paths and findings; `plan.md` has a summary and numbered tasks, each with Files, Depends on and Acceptance criteria. The verified run produced 176 ledger lines and eight tasks, from the `Vacancy` model through a manual Inspector verification pass, and changed no code; its files are in [vacancies-plan-solution/](./vacancies-plan-solution/).

> Note: In VS Code the same prompt works in the Plan agent (`/plan` followed by the prompt), which calls subagents through `#agent/runSubagent`. The Plan agent is read-only by default, so it cannot write the ledger until `github.copilot.chat.planAgent.additionalTools` grants it an edit tool.

---

## Step 2: Check the plan against the ledger

**Overview:** The plan is only as good as the findings behind it. Reading it against the ledger turns review from "does this sound right" into "which ledger line supports this".

**Research / Planning / Discussion:**

```text
Review demos/09-plan-spec-deliver/02-planning/vacancies-plan/plan.md against ledger.md in the same folder. For every acceptance criterion, quote the ledger line that supports it. List each criterion the ledger does not support, and each assumption the plan makes about how the running server behaves that nobody verified.
```

**Finding:** A good review quotes ledger lines rather than restating the plan. The criterion to look for is the database one: the plan expects `EnsureCreatedAsync` to create a `Vacancies` table, but `EnsureCreated` only builds a database that does not exist yet, so an existing `hr-data.db` never gets the new table. The server's readme says to delete `hr-data.db` to reseed; if the review does not raise this, ask it directly how the new table reaches a database that already exists.

**Recipe:**

```text
Update demos/09-plan-spec-deliver/02-planning/vacancies-plan/plan.md so every acceptance criterion is supported by ledger.md. Where the plan relies on EnsureCreatedAsync to add the Vacancies table, state that an existing src/hr-mcp-server/hr-data.db must be deleted so the schema is recreated and reseeded, and add that step to the verification task. Change nothing else.
```

**Expected Outcome:** `plan.md` still has the same numbered tasks. In the verified run the diff touched exactly two lines: the DbContext task's acceptance criteria now explain that `EnsureCreatedAsync` never alters an existing database, and the verification task now opens with deleting `hr-data.db`.

---

## Step 3: File the plan as a parent issue with sub-issues

**Overview:** A plan in a session folder is invisible to the team. The `create-issue` skill turns it into one parent issue and one sub-issue per task, labeled `planning`, so each task can be picked up or assigned to the Copilot coding agent on its own.

**Recipe:**

```text
/create-issue Turn demos/09-plan-spec-deliver/02-planning/vacancies-plan/plan.md into GitHub issues: one parent issue for the vacancies feature and one sub-issue per numbered task, all labeled planning. Create the planning label if it does not exist. Show me the issue tree before creating anything, then list every issue URL and confirm the sub-issue links.
```

**Expected Outcome:** Copilot shows the tree first: one parent titled for the vacancies feature and one child per plan task. After you approve, `gh label list` shows `planning`, the parent issue on GitHub shows a Sub-issues panel with every task in plan order, and the closing check lists the child numbers. The verified run created parent #60 with sub-issues #61 to #68:

```bash
gh api repos/{owner}/{repo}/issues/<parent-number>/sub_issues --jq '.[].number'
```

> The recipe above is one possible prompt based on typical findings from the research above. If your conversation led to different conclusions, use those instead.
