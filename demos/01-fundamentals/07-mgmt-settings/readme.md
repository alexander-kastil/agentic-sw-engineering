# Management and Settings

## Management policy features

Management policies allow administrators to set guardrails for how users can interact with Copilot. These policies can be configured at the organization, repository, or user level, and they provide control over features such as:

| Feature                                | Free & Pro | Business | Enterprise |
| -------------------------------------- | ---------- | -------- | ---------- |
| Public code filter                     | ✓          | ✓        | ✓          |
| User management                        | ✗          | ✓        | ✓          |
| Data excluded from training by default | ✗          | ✓        | ✓          |
| Enterprise-grade security              | ✗          | ✓        | ✓          |
| IP indemnity                           | ✗          | ✓        | ✓          |
| Content exclusions                     | ✗          | ✓        | ✓          |
| SAML SSO authentication                | ✗          | ✓        | ✓          |
| Require GitHub Enterprise Cloud        | ✗          | ✗        | ✓          |
| Usage metrics                          | ✗          | ✓        | ✓          |

## Customization features

| Feature                                                      | Free & Pro | Business | Enterprise |
| ------------------------------------------------------------ | ---------- | -------- | ---------- |
| Tailor chat conversations to your private codebase           | ✗          | ✗        | ✓          |
| Unlimited integrations with Copilot Extensions (public beta) | ✓          | ✓        | ✓          |
| Build a private extension for internal tooling (public beta) | ✓          | ✓        | ✓          |
| Attach knowledge bases to chat for organizational context    | ✗          | ✗        | ✓          |

## Filtering out matching public code

| Scope                                                  | Who can manage  | What it controls                                              | Notes                                                                                                                                         |
| ------------------------------------------------------ | --------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Organization (Business/Enterprise plans)               | Admins          | Public Code filter for all members; required for IP indemnity | Organization admins can block suggestions matching public code for all members. This is required to activate Intellectual Property Indemnity. |
| Personal account (Free, Pro, Pro+) – individually paid | Individual user | Toggle to Allow or Block suggestions matching public code     | Users who purchase their own Copilot license can fully control this setting in their personal account under Copilot → Features → Privacy.     |
| Personal account (Free, Pro, Pro+) – org-provided      | Individual user | Toggle to Allow or Block suggestions matching public code     | If your seat is assigned by an organization, the toggle may be locked and will reflect the organization's policy.                             |

## Credentials and Permissions

### Credential Security

GitHub Copilot does not have built-in credential or environment variable blacklist/whitelist features. However, you can control what Copilot accesses through these approaches:

| Method | Scope | Control Level |
|--------|-------|---------------|
| `.gitignore` exclusion | Workspace | Prevents secrets from being tracked or shared |
| VS Code file disabling | Editor | Disables Copilot for specific file patterns (`.env`, `*.secrets`) |
| Custom instructions | Agent behavior | Add explicit security guidelines to prevent credential inclusion |
| Workspace trust | IDE level | Untrusted workspaces limit extension functionality |
| Environment isolation | System level | Secrets stored separately from workspace context |

### Best Practices

1. **Store secrets securely**
   - Use `.env` files and add to `.gitignore`
   - Never commit credentials to git repositories
   - Use VS Code's Secrets Storage API for extensions

2. **Configure workspace settings**
   ```json
   {
     "github.copilot.enable": {
       "*": true,
       ".env": false,
       "*.secrets": false,
       "*.private": false
     }
   }
   ```

3. **Use placeholders in code**
   - Replace real API keys with `PLACEHOLDER_KEY` in examples
   - Reference environment variables by name rather than value

4. **Set explicit Copilot rules**
   - Add security guidelines to `.instructions.md`
   - Flag never to include credentials, API keys, or secrets in suggestions
   - Require mock/placeholder values in code examples

5. **Leverage VS Code security features**
   - Enable workspace trust to control extension permissions
   - Restrict Copilot access to sensitive files and directories
   - Use untrusted workspace mode for external/untrusted projects

### What Copilot Can Access

- Open editor files and workspace content
- Files explicitly shown in chat or context
- Terminal output displayed in VS Code
- Selected code snippets you share

**Key consideration**: Copilot only sees what you show it. Properly configured workspace settings and `.gitignore` are the primary defenders against credential exposure.
