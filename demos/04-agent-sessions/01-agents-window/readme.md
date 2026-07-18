# The Agents Window

The Agents window is a dedicated companion window, introduced as a preview in VS Code 1.120, for running agents across multiple projects at once. It sits beside your editor rather than inside it, so agent work no longer competes with the file you are reading for screen space. Each window is independent: you can point one at a different model, a different project, or a different execution host while the others keep running.

The window matters because agentic work is no longer a single blocking conversation in the sidebar. A selectable agent harness lets you choose which backend runs a given session, remote execution lets that session run away from your laptop, and per-window setting overrides let each window carry its own configuration. Extensions opt in to appearing in the window through the `extensions.supportAgentsWindow` capability, so tools you already use can surface their agent surfaces here.

## Capabilities in the Preview

| Capability | What it gives you |
|---|---|
| Companion window | A separate window for agent sessions, kept out of the main editor layout |
| Selectable harness | Choose which agent backend runs a session, per window |
| Remote execution | Run a session on a remote host instead of the local machine |
| Per-window overrides | Model, project, and host settings scoped to one window |
| `extensions.supportAgentsWindow` | The capability an extension declares to appear in the window |

## How One Window Differs From the Next

The value of separate windows is that each one carries its own context and target. A window overriding the model and host does not change what any other window is doing, which is what makes several projects viable at the same time.

```mermaid
flowchart LR
    E["VS Code editor"] --> W1["Agents window A<br/>project X, local host"]
    E --> W2["Agents window B<br/>project Y, remote host"]
    W1 --> H1["Harness A"]
    W2 --> H2["Harness B"]
```

> Note: The Agents window shipped as a preview in VS Code 1.120. Preview surfaces move quickly, so confirm the exact toggles against the release notes for the version you are running before relying on a specific setting.

## Exercise

1. Update to VS Code 1.120 or later and open a workspace you use for agent work.
2. Open the Command Palette and search for the Agents window command to launch the companion window.
3. Start a session in the window and confirm it runs independently of the editor sidebar chat.
4. Open a second Agents window and point it at a different project or model using the per-window settings.
5. Confirm both windows run their sessions in parallel without interfering with each other.

## Links & Resources

- [VS Code 1.120 release notes](https://code.visualstudio.com/updates/v1_120) - the Agents window preview, selectable harness, and per-window overrides
- [Copilot in VS Code documentation](https://code.visualstudio.com/docs/copilot/overview) - how Copilot agent surfaces integrate with the editor
