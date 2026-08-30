# Building a Multi-Agent System

One agent handles one job well; hard problems need several agents that each own a part and hand work to each other. The Copilot SDK gives you the building blocks: independent sessions, custom tools, and a client you can drive from orchestration code. This topic composes them into a coordinated system rather than a single assistant.

## The pattern

A coordinator agent breaks a request into parts and delegates each to a specialized agent: a researcher that gathers facts, a builder that writes code, a reviewer that checks it. Each specialist runs in its own session with its own tools, and the coordinator passes results between them. Because every agent is just an SDK session, you scale the system by adding specialists, not by growing one prompt.

## Why it beats one big agent

Splitting the work keeps each agent's context focused, makes failures easier to isolate, and lets you run independent parts in parallel. It mirrors the multi-agent orchestration you saw in Implementing Agentic Coding, applied here in code you own end to end.

## Exercise

1. Define two specialist agents with distinct tools, for example a researcher and a reviewer.
2. Write a coordinator that calls each in turn and passes the first result into the second.
3. Add a third specialist and confirm the coordinator routes to it without changing the others.

## Links & Resources

- [GitHub Copilot SDK Repository](https://github.com/github/copilot-sdk) - sessions, tools, and multi-agent samples in the cookbook
- [Custom Tools Documentation](https://github.com/github/copilot-sdk/blob/main/docs/guides/tools.md) - the tool interface each specialist agent uses
