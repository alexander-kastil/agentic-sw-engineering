# Agent Host Protocol (AHP vs ACP)


The Agent Host Protocol (AHP) is an open specification where authoritative session state lives on a long-lived host and synchronizes out to one or more clients. Because the host outlives any single client, sessions survive disconnects and reconnect cleanly. This is an architect-track topic: the point is the boundary between where state lives and where you view it, not a set of buttons to click.

The design contrast worth internalizing is AHP against the Agent Client Protocol (ACP). Under a client-authoritative model, the session lives with the client, so closing the client risks losing the running work. Under AHP, the host is authoritative, the client is a view, and the same session can be attached from more than one place. The agent host is built on the Copilot SDK, which makes the SDK load-bearing for this whole module and links directly to [Module 5](../../05-cli-sdk/02-sdk/01-intro/).

## AHP vs ACP at a Glance

| Dimension | Agent Client Protocol (ACP) | Agent Host Protocol (AHP) |
|---|---|---|
| Authoritative state | Lives with the client | Lives on the host |
| Host lifetime | Bound to the client session | Long-lived, outlives clients |
| Disconnect behavior | Risk of losing running work | Session survives, reconnects cleanly |
| Client role | Owns the session | A view onto host state |
| Number of viewers | Typically one | One or more |

## Host-Authoritative State

Treat the host as the source of truth and every client as a window onto it. A client can drop off the network, come back, and resynchronize because the host never stopped tracking the session.

```mermaid
flowchart LR
    H["Long-lived host<br/>authoritative state"] --> C1["Client A<br/>view"]
    H --> C2["Client B<br/>view"]
    C1 -. "reconnects" .-> H
    C2 -. "reconnects" .-> H
```

Because the host is built on the Copilot SDK, the same primitives that let you build an agent programmatically are the ones running the session behind the editor. That is why the SDK topic in Module 5 is not an optional aside: it describes the foundation this protocol stands on.

## What Runs on the Host

The host is not something you switch on. Every session you start in the Agents window already runs on it, and the harness is a chip in the composer next to the workspace: Copilot, Claude, and Codex all run on the same host. The Copilot agent there is powered by the Copilot SDK, so its behavior matches the Copilot CLI and the standalone GitHub Copilot app instead of diverging per surface. Because the host outlives any window, one session can be attached from several VS Code windows at the same time.

What you can configure is which harnesses and hosts are available, not the protocol itself:

| Setting | What it controls |
|---|---|
| `chat.agentHost.claudeAgent.enabled` | Whether the Claude harness is offered in the composer |
| `chat.agentHost.codexAgent.enabled` | Whether the Codex harness is offered |
| `chat.agentHost.allowSignedOutWhenUsable` | Opens the Agents window with an existing Claude API key and no GitHub sign-in, the offline path described in [Selecting Models](../../01-fundamentals/02-models/) |
| `chat.agentHost.forwardSSHAgent` | Forwards your SSH agent to a remote host, so a session there can reach your Git remotes |
| `chat.agentHost.devContainer.enabled` | Lets a session run inside a dev container rather than on the host directly |

## Agent Host Protocol 1.0 and Delegation to Remote Hosts

Since VS Code 1.144 the first version of the Agent Host Protocol is published. It is the protocol VS Code uses to talk to its agents, locally and on remote machines, and cloud automations use it as well. Because it is open and extensible, you can build custom UIs for agents, or agent platforms that plug into any UI that speaks it, and libraries exist in six languages.

To connect a second machine, run **Agents: Add Remote Agent Host...** in the Agents window, which adds a websocket-based agent host. To see where your own editor's running agent host listens, run `code agent endpoints` in a terminal; it prints the endpoints. Once hosts are connected, one session can hand work to another, which is the delegation this topic adds on top of attaching more clients.

Since VS Code 1.140 (Experimental), the settings `chat.remoteAgentHostsEnabled` and `chat.remoteSessions.tools.enabled` give the agent four tools for that delegation.

| Tool | What it does |
|---|---|
| `list_agent_hosts` | Lists hosts with their models, capacity, and session load |
| `create_remote_session` | Starts a session on a named host, or places it automatically by OS, minimum memory, logical CPUs, and optional model; it favors the host with the fewest running sessions |
| `get_remote_session` | Returns a session's status and latest response |
| `send_remote_message` | Sends follow-up work to the remote session, or results and questions back to the originating chat |

A few rules shape how you use them. A remote session has no workspace unless you name one: an existing trusted folder on the host, either directly or in a new Git worktree. The tools do not clone or copy the originating workspace, so the code must already be on the target host. Normal approvals apply, and you keep the coordinating Agents window open.

Remote agents report back through `send_remote_message`, and their final answers are not forwarded automatically. Ask for the report in your prompt, as the demo below does. Name a host when the work needs a specific toolchain, and let automatic placement choose when any machine that fits will do. The coordinating chat stays the place where you read results and decide what happens next.

Together the pieces turn the host from a place where state lives into a pool of machines an agent can choose from.

## Demo

Prove that the session, not the window, owns the work.

1. Open the Agents window with the **Open in Agents** button in the title bar, `Chat: Open Agents window` from the Command Palette, or `code --agents`.
2. Select **New** (`Ctrl+N`) and start a task long enough to still be running a minute from now, such as a refactor spanning several files.
3. Close the window while the agent is still working, which under a client-authoritative model would end the run.
4. Reopen the Agents window. The session is in the Sessions list, still running, carrying the turns that completed while no client was attached.
5. Open the same session in a second window and confirm both views track one session rather than forking into two.
6. Switch the harness chip in the composer from Copilot to Claude or Codex and start another session, confirming the host is shared infrastructure rather than a Copilot-only feature.
7. Enable the delegation tools in your user settings.

   ```json
   {
     "chat.remoteAgentHostsEnabled": true,
     "chat.remoteSessions.tools.enabled": true
   }
   ```

   Run **Agents: Add Remote Agent Host...** to connect a host, then start a session with this prompt.

   ```text
   Start a remote session on a connected Linux host with at least 16 GiB of memory and eight logical CPUs. Check the installed Node.js and Python versions and report back to this chat.
   ```

   Expected result: the agent lists the hosts, creates a remote session on a host that fits, and the versions come back to this chat through `send_remote_message`.

## Links & Resources

- [Understand the VS Code Agent Host](https://code.visualstudio.com/docs/agents/concepts/agent-host) - the host process, its lifetime, and what attaches to it
- [Understand agent sessions and handoff](https://code.visualstudio.com/docs/agents/concepts/sessions) - what a session owns and how it moves between clients
- [Agent Host Protocol](https://microsoft.github.io/agent-host-protocol/) - the open specification and its libraries
- [Introducing the Agent Host](https://code.visualstudio.com/blogs/2026/08/26/agent-host-architecture) - why state moved off the client

[← Previous: The Agents Window](../01-agents-window/readme.md) | [Back to Agent Sessions](../readme.md) | [Next: Remote Agent Sessions over SSH & Dev Tunnels →](../03-remote-sessions/readme.md)
