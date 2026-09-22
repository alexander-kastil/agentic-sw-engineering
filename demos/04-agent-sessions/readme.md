# Agent Sessions & Agents Window

## The Session-Centric Product

GitHub Copilot has moved from an in-editor assistant to an agent-session model, and the Agents window is the companion surface where that model lives. Having put agents to work in Implementing Agentic Coding, you now meet the infrastructure underneath the runs you just drove: the window, the Agent Host Protocol beneath it, remote sessions, and the day-to-day mechanics of running many sessions safely. You run agents across multiple projects, drive them locally or on remote hosts, and manage their sessions as first-class, long-lived objects.

| Topic | Description |
|-------|-------------|
| [The Agents Window](./01-agents-window/) | The dedicated companion window for running agents across projects, with a selectable harness and per-window overrides. |
| [Agent Host Protocol (AHP vs ACP)](./02-host-protocol/) | How host-authoritative session state works, contrasted with the Agent Client Protocol. |
| [Remote Agent Sessions over SSH & Dev Tunnels](./03-remote-sessions/) | Reproducible, cloud-backed environments that replace the Codespaces workflow. |
| [Managing Sessions in the Agents Window](./04-session-management/) | Side-by-side sessions, groups, background send, banners, multi-chat, `/chronicle`, and `/troubleshoot`. |

Subagents are covered where you use them, in [Multi-Agent Orchestration with Subagents](../03-agentic-coding/03-orchestration/).

## Helpful Copilot Slash Commands

These commands are specific to running and inspecting agent sessions. They are read-first: none of them changes your code on its own, which makes them safe to reach for while a session is live.

| Command | Usage |
|---|---|
| `/chronicle` | Query your session history: `standup` for a summary, `search` by file or PR, `reindex` when results look thin |
| `/troubleshoot` | Analyze the session's own record to diagnose a stall or a failed tool call |
| `/btw` | Ask a side question without interrupting the running turn |

> Note: The Sessions picker (Ctrl+R) is not a slash command but pairs well with these; use it to jump between the many sessions the commands above help you recall and repair.

## Key Topics covered in this module

- [The Agents Window](./01-agents-window/)
- [Agent Host Protocol (AHP vs ACP)](./02-host-protocol/)
- [Remote Agent Sessions over SSH & Dev Tunnels](./03-remote-sessions/)
- [Managing Sessions in the Agents Window](./04-session-management/)
