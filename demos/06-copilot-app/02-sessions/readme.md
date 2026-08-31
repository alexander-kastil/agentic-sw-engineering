# Sessions from Issues, Prompts & Pull Requests

A session in the Copilot app starts from one of three entry points: a GitHub issue, a freeform prompt, or a pull request already in flight. This mirrors how real work arrives, so you open a session from the artifact you already have rather than describing the task from scratch. An issue carries the acceptance criteria, a PR carries the diff and review comments, and a prompt is the escape hatch for work that does not yet have a tracking artifact.

Each session runs in an isolated space with its own branch and files, so parallel sessions never interfere with each other. When you open a session you choose how that space is created: a new worktree, or a local repository clone. This isolation is what makes it safe to run several agents against the same repository at the same time, which is the whole reason to work in a dedicated agents view.

The worktree and clone options differ in how they relate to your existing local checkout. A worktree is a linked working directory of the same repository, sharing history while keeping a separate branch and files. A local repository is a separate clone. Both give the session a clean, independent place to work.

Two settings save you from answering the same question every time. A worktree toggle switches worktrees on or off for all repositories at once when starting a session, and a worktree location setting decides where those directories are created. Point the location at a fast local disk rather than a synced folder, and a session that checks out a large repository stops paying for someone else's file watcher.

## Session entry points

| Start from | You get | Best when |
|---|---|---|
| A GitHub issue | The issue's context and acceptance criteria as the task | The work is already tracked and specified |
| A freeform prompt | A blank task you describe in natural language | There is no issue or PR yet |
| A pull request in flight | The existing branch, diff, and review comments | You are iterating on or finishing open work |

> Note: Starting from an issue or PR pulls in the surrounding GitHub context automatically, so the agent begins with the acceptance criteria or the existing diff instead of a blank slate.

## How a session gets its isolated space

```mermaid
flowchart LR
    A["Pick entry point<br/>issue, prompt, or PR"] --> B{"Choose space"}
    B -->|"New worktree"| C["Linked working dir<br/>own branch and files"]
    B -->|"Local repository"| D["Separate clone<br/>own branch and files"]
    C --> E["Agent runs<br/>isolated from other sessions"]
    D --> E
```

A session is not limited to one checkout for its whole life either. You can create a child session inside an existing project checkout, which is the cheap way to split a task that grew a second front without paying for another clone.

## Inside a running session

A session is more than a chat transcript. Alongside the conversation it carries a **Files** tab for the working tree, a **Plan** tab for the steps the agent intends to take, and a **background tasks** tab for work that is still running. Reading the Plan tab before the agent gets far is the cheapest correction you will ever make, because steering a plan costs one sentence and steering a finished diff costs a review.

Side questions no longer cost you the run. `/ask` and `/btw` put a question to the agent without interrupting the response in progress, and a side chat lets you explore an option in parallel with the main thread. Use it when the agent asks you something and you want to think out loud before committing to an answer.

```mermaid
flowchart LR
    A["A session"] --> B["Chat<br/>the main thread"]
    A --> C["Files, Plan,<br/>background tasks"]
    A --> D["Side chat<br/>/ask and /btw"]
```

> Note: A session started here is not stuck here. With `chat.agentSessions.showExternal` (VS Code 1.135), VS Code's Sessions list shows recent Copilot and Claude sessions created in other applications and lets you continue them in the editor.

## Exercise

Practice opening the three kinds of session in the Copilot desktop app and confirming their isolation.

1. Install and open the GitHub Copilot desktop app on your platform, and sign in with a GitHub account that has a Copilot plan or configure a bring-your-own-key endpoint.
2. Set the **worktree location** to a fast local path, and turn the all-repositories worktree toggle on so new sessions stop asking.
3. Start a session from a **prompt**: create a new session and describe a small, safe task such as "add a short section to the README explaining how to run the app".
4. While it runs, open the **Plan** tab and read the steps the agent intends to take; use `/btw` to ask a clarifying question without interrupting the run.
5. Start a second session from an **issue**: pick an existing issue in a repository you own, open it as a session, and confirm the agent begins with the issue's title and body as its task.
6. Start a third session from a **pull request** that is already in flight, and confirm the session opens on that PR's branch with its existing changes present.
7. With all three sessions running, confirm they do not collide: each has its own branch and files, so a change in one does not appear in the others.
8. Turn on `chat.agentSessions.showExternal` in VS Code, find one of these app sessions in its Sessions list, and continue the conversation there.

## Links & Resources

- [GitHub Copilot app](https://github.com/features/ai/github-app) - sessions from issues, prompts, and PRs, and the worktree vs local repository choice
- [Working with GitHub issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) - the issues that seed a session's task and acceptance criteria
- [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) - the in-flight PRs a session can continue
- [VS Code 1.135 release notes](https://code.visualstudio.com/updates/v1_135) - external agent sessions surfaced and continued in VS Code
