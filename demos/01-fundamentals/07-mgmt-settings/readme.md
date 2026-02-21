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
