# Codebase Q&A and Onboarding

The fastest way to learn an unfamiliar codebase is to ask it questions, and the Copilot CLI does exactly that from the terminal. Point it at a repository and it reads the code as context, so you can trace how a feature works, find where a behavior lives, and understand the architecture without clicking through hundreds of files. This turns a multi-day onboarding into a conversation.

## Ask the codebase

Launch the CLI in a project and ask in natural language: where a request enters the system, how authentication is enforced, which module owns a piece of logic. The agent searches the code, follows the references, and answers with the concrete files and lines, so you can jump straight to what matters. Use it to build a mental map before you change anything.

## Onboarding output

Beyond one-off answers, ask the CLI to produce a short architecture overview, a "start here" guide for a subsystem, or a list of the key entry points and their responsibilities. A new team member gets a grounded tour of the actual code rather than a stale wiki page.

## Exercise

1. Open the CLI in a repository you do not know well and ask how one feature works end to end.
2. Follow the files and lines it cites and confirm the answer against the real code.
3. Ask it to write a short onboarding overview of one subsystem, and check it for accuracy.

## Links & Resources

- [About Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) - how the CLI uses your codebase as context
- [GitHub Copilot CLI Repository](https://github.com/github/copilot-cli) - source, releases, and usage examples
