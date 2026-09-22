# The SSH MCP server

`ssh-mcp` gives an agent a persistent shell session on a remote host as an MCP tool, instead of composing a fresh `ssh` command for every step. The target is pinned in configuration, so the agent cannot aim a command at the wrong machine.

## Configuration

The server is registered per repository in `.mcp.json`. Key authentication:

```json
{
  "mcpServers": {
    "ssh-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "ssh-mcp",
        "--",
        "--host=<HOST_OR_IP>",
        "--port=22",
        "--user=<USER>",
        "--key=<ABSOLUTE_PATH_TO_PRIVATE_KEY>",
        "--timeout=120000",
        "--maxChars=none"
      ]
    }
  }
}
```

Password authentication replaces `--key` with `--password` and, where privileged commands are needed, `--sudoPassword`. Use it only for a disposable lab host.

| Flag | Purpose |
|------|---------|
| `--host` | Target address or hostname. Pinned per repository. |
| `--port` | SSH port, `22` unless the host was moved off it. |
| `--user` | Remote account. |
| `--key` | Absolute path to the private key. Mutually exclusive with `--password`. |
| `--password` | Password for the account. Never for a hardened host. |
| `--sudoPassword` | Supplied when a command needs elevation. |
| `--timeout` | Milliseconds. Raise it for image builds, which routinely exceed the default. |
| `--maxChars` | Output cap. `none` keeps full build and log output. |

Registering more than one server is how you reach more than one box. Name them for the target, for example `ssh-mcp-staging` and `ssh-mcp-prod`, so the agent picks by name rather than by editing configuration.

## Handshake failures are almost always configuration

A handshake that times out reads like a network problem and usually is not. Check these in order before touching the host.

The configured `--host` may not be the machine you are working on. The pin is per repository and is easy to inherit from an older project, so a server left pointing at a decommissioned address times out against a perfectly healthy target.

The host may not accept the configured authentication method. A hardened box sets `PasswordAuthentication no`, so a password-configured server never completes the handshake regardless of whether the password is correct. Switch to `--key`.

The key path may be wrong or unreadable. An absolute path is required, and a `~` is not expanded by every launcher. On Windows use forward slashes inside the JSON value.

The timeout may simply be too short for the command. A first `docker build` on a small host can exceed two minutes, and the resulting error is indistinguishable from a connection failure.

## Falling back to plain ssh

When the MCP server cannot be made to work, drop to the OpenSSH client for the same operations. This also isolates the failure: if plain `ssh` succeeds with the same credentials, the problem is the server configuration.

```bash
ssh -i <KEY> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new <USER>@<HOST> '<command>'
scp -i <KEY> <local-path> <USER>@<HOST>:<remote-path>
```

`IdentitiesOnly=yes` matters. Without it the client offers every default key first, and a host with a low `MaxAuthTries` closes the connection before reaching the key you specified.

## Security posture

The configuration file holds a live credential in cleartext. Add it to `.gitignore`, commit a `.mcp.json.example` carrying placeholder values, and hand real values to teammates through the same channel you use for any other secret.

A server configured with `--sudoPassword` grants the agent root on that host. Scope it to hosts where that is acceptable, and prefer a dedicated account with a narrow sudoers entry over the root account.
