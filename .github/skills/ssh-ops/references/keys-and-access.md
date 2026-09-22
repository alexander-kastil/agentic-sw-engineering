# Keys and access

Authentication failures on a healthy host come from a small number of causes, and every one of them is checkable from the client side.

## Generate a key

Ed25519 is the default choice: short, fast, and supported by everything current.

```bash
ssh-keygen -t ed25519 -C "<comment>" -f ~/.ssh/<key-name>
```

```powershell
ssh-keygen -t ed25519 -C "<comment>" -f "$env:USERPROFILE\.ssh\<key-name>"
```

The private key stays on the client and is never copied anywhere. Only `<key-name>.pub` is installed on hosts.

## Install the public key on a host

```bash
ssh-copy-id -i ~/.ssh/<key-name>.pub <USER>@<HOST>
```

Where `ssh-copy-id` is unavailable, append the public key to `~/.ssh/authorized_keys` on the host and then fix the permissions, which sshd enforces strictly.

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

A key that looks correct but is rejected on every attempt is usually a permissions problem on the host, not the wrong key.

## Match by fingerprint, not by filename

A key file named for one host is frequently the key registered elsewhere under a different name. Compare fingerprints rather than trusting the filename.

```bash
ssh-keygen -l -f ~/.ssh/<key-name>
ssh-keygen -l -f ~/.ssh/authorized_keys
```

Run the second command on the host to list which fingerprints it actually trusts, then look for yours in the output.

## A host built before the key existed never received it

When a provider injects keys at creation time, a host created before a key was registered does not have it, and no amount of retrying changes that. Compare the age of the host against the age of the key. Recovering access means using the provider's rescue mode or serial console to append the key manually.

## Always test with IdentitiesOnly

```bash
ssh -i ~/.ssh/<key-name> -o IdentitiesOnly=yes -o BatchMode=yes <USER>@<HOST> 'echo ok'
```

Without `IdentitiesOnly=yes` the client offers every key in the agent and in `~/.ssh` before the one you named. A host running the default `MaxAuthTries 6` can close the connection first, producing a `Permission denied (publickey)` that has nothing to do with the key you specified. `BatchMode=yes` stops a password prompt from hanging a non-interactive session.

## Pin the host in ssh config

Once a host works, record it so neither you nor the agent has to reassemble the flags.

```
Host <alias>
    HostName <HOST_OR_IP>
    User <USER>
    IdentityFile ~/.ssh/<key-name>
    IdentitiesOnly yes
```

The connection becomes `ssh <alias>`, and a changed address is a one-line edit rather than a search through scripts.

## Host key changes

A `REMOTE HOST IDENTIFICATION HAS CHANGED` warning after a rebuild is expected, because the host generated new host keys. After a rebuild you did not perform it is not expected, and is worth investigating before connecting. Remove the stale entry deliberately.

```bash
ssh-keygen -R <HOST_OR_IP>
```

Never set `StrictHostKeyChecking no` to make the warning go away. Use `accept-new`, which trusts a first-time host but still refuses a changed one.
