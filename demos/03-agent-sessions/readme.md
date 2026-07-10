# Agent Sessions & Agents Window

## The Session-Centric Product

GitHub Copilot has moved from an in-editor assistant to an agent-session model, and the Agents window is the companion surface where that model lives. You run agents across multiple projects, drive them locally or on remote hosts, and manage their sessions as first-class, long-lived objects. This module covers the window, the Agent Host Protocol beneath it, remote sessions, and the day-to-day mechanics of running many sessions safely.

| Topic | Description |
|-------|-------------|
| [The Agents Window](./01-agents-window/) | The dedicated companion window for running agents across projects, with a selectable harness and per-window overrides. |
| [Agent Host Protocol (AHP vs ACP)](./02-host-protocol/) | How host-authoritative session state works, contrasted with the Agent Client Protocol. |
| [Remote Agent Sessions over SSH & Dev Tunnels](./03-remote-sessions/) | Reproducible, cloud-backed environments that replace the Codespaces workflow. |
| [Session Management](./04-session-management/) | Side-by-side sessions, groups, background send, banners, and multi-chat. |
| [Session Persistence & /chronicle](./05-persistence/) | Sync sessions to your GitHub account and query past work for standup reports. |
| [Subagents](./06-subagents/) | Built-in subagents, read-only peer transcripts, and per-subagent credit cost. |
| [Deep Research with /research](./07-research/) | A read-only deep-research agent that produces a cited Markdown report. |
| [Troubleshooting Agent Sessions](./08-troubleshooting/) | Diagnose local and remote agent-host sessions with /troubleshoot. |

## Helpful Copilot Slash Commands

These commands are specific to running and inspecting agent sessions. They are read-first: none of them changes your code on their own, which makes them safe to reach for while a session is live.

| Command | Usage |
|---|---|
| `/research` | Run the read-only deep-research agent and get a cited Markdown report before touching any code |
| `/chronicle` | Query your synced session history for a standup report or the sessions that touched a file or PR |
| `/troubleshoot` | Analyze a local or remote agent-host session's logs to diagnose a stall or a failed tool call |

> Note: The session picker (Ctrl+R) is not a slash command but pairs well with these; use it to jump between the many sessions the commands above help you research, recall, and repair.

## Key Topics covered in this module

- [The Agents Window](./01-agents-window/)
- [Agent Host Protocol (AHP vs ACP)](./02-host-protocol/)
- [Remote Agent Sessions over SSH & Dev Tunnels](./03-remote-sessions/)
- [Session Management](./04-session-management/)
- [Session Persistence & /chronicle](./05-persistence/)
- [Subagents](./06-subagents/)
- [Deep Research with /research](./07-research/)
- [Troubleshooting Agent Sessions](./08-troubleshooting/)
