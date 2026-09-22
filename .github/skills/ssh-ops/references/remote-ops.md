# Operating the box

Procedures for running commands, moving files, and deploying to a remote host once the connection works.

## Probe before you act

The first command of any session is read-only and proves the transport, the account, and the shape of the host in one call.

```bash
cat /etc/os-release | head -2
uname -r
df -h /
docker --version 2>/dev/null || echo "docker: not installed"
systemctl --failed --no-pager
```

Everything after this can assume a working session, which means a later failure is about the command rather than the connection.

## Read a failed connection in order

Four causes produce nearly identical symptoms. Distinguish them from the client without touching the host.

| Check | Command | What it rules out |
|-------|---------|-------------------|
| Configured target | Read `--host` in `.mcp.json` or `HostName` in ssh config | Pointing at the wrong or a decommissioned machine |
| Route to the address | `tracert -d -h 8 <HOST>` or `traceroute -m 8 <HOST>` | No route, wrong network, VPN down |
| Port reachable | `bash -c 'echo > /dev/tcp/<HOST>/22'` | Host down, firewall, sshd stopped |
| Auth method | `ssh -v -o IdentitiesOnly=yes -i <KEY> <USER>@<HOST>` | Wrong key, password auth disabled |

A private RFC1918 address whose trace leaks out to the public internet has no route from where you are. That is a network or subnet problem, not a firewall on the host, and rebooting the box fixes nothing.

Do not scan a subnet looking for the host. It reads as reconnaissance, and on a managed network it gets the source address blocked.

## Deploy when the box has a git checkout

```bash
ssh <alias> 'cd <REMOTE_PATH> && git pull && docker compose up -d --build <service>'
```

Rebuild the single affected service rather than the whole stack. A full rebuild on a small host is slow enough that the timeout expires and the operation looks failed while it is still running.

## Deploy when the box has no git checkout

A host provisioned from a synced source tree has no `.git`, so `git pull` silently does nothing useful. Probe first, then copy the source and build on the box.

```bash
ssh <alias> 'test -d <REMOTE_PATH>/.git && echo "checkout" || echo "no checkout"'
scp -r ./src <USER>@<HOST>:<REMOTE_PATH>/
ssh <alias> 'cd <REMOTE_PATH> && docker compose up -d --build <service>'
```

Copy only the subtree that changed. Sending the whole repository pushes build artifacts and dependencies across the wire and can fill a small disk.

## Prove it, do not claim it

A deployment is finished when a health check returns, not when the build exits zero.

```bash
ssh <alias> 'docker compose ps --format "{{.Service}} {{.State}} {{.Status}}"'
curl -sf -o /dev/null -w '%{http_code}\n' https://<HOST_OR_DOMAIN>/health
```

Report the actual response. A summary that says the stack is healthy without the output of one of these commands is a claim, not a verification.

## Long-running commands

Anything that outlives the session needs to be detached, or the connection dropping kills it.

```bash
ssh <alias> 'nohup <command> > /var/log/<name>.log 2>&1 &'
ssh <alias> 'tail -n 50 /var/log/<name>.log'
```

Raise the client timeout for builds instead of detaching them when you need the output inline. A truncated build log is worse than a slow one.

## Keep the session alive on a flaky link

```
Host <alias>
    ServerAliveInterval 30
    ServerAliveCountMax 6
```

This sends a keepalive every 30 seconds and tolerates three minutes of silence before giving up, which covers most transient drops without masking a genuinely dead host.
