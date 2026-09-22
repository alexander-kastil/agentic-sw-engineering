# Codebase Q&A and Onboarding

The fastest way to learn an unfamiliar codebase is to ask it questions, and the Copilot CLI does exactly that from the terminal. Point it at a repository and it reads the code as context, so you can trace how a feature works, find where a behavior lives, and understand the architecture without clicking through hundreds of files. This turns a multi-day onboarding into a conversation.

## Ask the codebase

Launch the CLI in a project and ask in natural language: where a request enters the system, how authentication is enforced, which module owns a piece of logic. The agent searches the code, follows the references, and answers with the concrete files and lines, so you can jump straight to what matters. Use it to build a mental map before you change anything.

## Onboarding output

Beyond one-off answers, ask the CLI to produce a short architecture overview, a "start here" guide for a subsystem, or a list of the key entry points and their responsibilities. A new team member gets a grounded tour of the actual code rather than a stale wiki page.

## Demo

1. Open the CLI in a repository you do not know well and ask how one feature works end to end.

```bash
copilot -C /path/to/unfamiliar-repo
```

2. Follow the files and lines it cites and confirm the answer against the real code. Pull a specific file into the conversation with `@`, and run your own checks with `!` without handing the turn to the agent.
3. Ask it to write a short onboarding overview of one subsystem, and check it for accuracy.
4. Capture the answer for a colleague with `/share`, which writes the session to a Markdown file, an HTML file, a gist, or a shareable link.

> Note: `copilot init` writes an `AGENTS.md` for the repository, so the next question starts from a grounded description of the project instead of a cold read.

## Links & Resources

- [About Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) - how the CLI uses your codebase as context
- [Using Copilot CLI](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli) - working directories, file mentions, and sharing a session
- [GitHub Copilot CLI repository](https://github.com/github/copilot-cli) - releases, changelog, and usage examples
