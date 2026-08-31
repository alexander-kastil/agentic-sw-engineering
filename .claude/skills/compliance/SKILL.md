---
name: compliance
description: >-
  Master skill for regulatory compliance assessment of a product: routes to the
  matching leaf and covers both the AI-specific and the personal-data regulations.
  Leaf `eu-ai-act` handles EU AI Act risk-tier classification (prohibited / high-risk /
  limited-risk transparency / minimal), the Article 50 transparency-disclosure pattern
  for consent screens and Terms of Service, and stakeholder/owner checklists. Leaf
  `dsgvo` handles DSGVO / GDPR personal-data compliance: lawful basis, data-subject
  rights, privacy notice, processor (Art. 28) agreements, records of processing,
  DPIA, breach notification, third-country transfers, and the compliance-check
  checklist. Use when asked to "check compliance", "compliance checklist", "EU AI Act
  compliance", "is our AI high-risk", "Article 50 transparency", "DSGVO compliance",
  "GDPR compliance", "check for DSGVO", "are we GDPR compliant", "do we need a privacy
  notice / Datenschutzerklärung", "lawful basis", "data subject rights", "data
  processing agreement", "AVV", "DPIA", "data breach 72 hours", "third-country
  transfer", "is DeepInfra DSGVO/GDPR compliant", "DeepInfra data privacy", "can we
  use DeepInfra with personal data", or when adding a feature that collects personal
  data or uses AI that touches people. Leaf `accessibility-a11y` handles web
  accessibility compliance: the EU Accessibility Act / Web Accessibility Directive /
  Austrian Barrierefreiheitsgesetz frame, WCAG 2.1 AA as the conformance target, the
  best-practice checklist (semantic HTML, ARIA, contrast, focus, keyboard, images,
  responsive, testing), an audit workflow, and fix recipes for legacy and CMS-exported
  static sites. Use when asked to "check accessibility", "a11y audit", "WCAG
  compliance", "is this site accessible", "EAA / Barrierefreiheit", or "fix
  accessibility findings".
metadata:
  type: reference
---

# compliance — regulatory compliance assessment (router)

Master skill for assessing and documenting a product's regulatory compliance. It owns two
leaves, one per regulation, and routes work to the one (or both) in scope. Route to the leaf
rather than answering inline; when a feature both uses AI and touches personal data, run **both**.

## Leaves

| Leaf | File | Owns |
| --- | --- | --- |
| **EU AI Act** | `references/eu-ai-act.md` | AI-specific regulation: risk-tier classification, the Article 50 transparency-disclosure pattern for consent/ToS, stakeholder and owner checklists, the phased compliance timeline. |
| **DSGVO / GDPR** | `references/dsgvo.md` | Personal-data regulation (EU 2016/679, Austrian DSG): lawful basis, the seven principles, data-subject rights, privacy notice, Art. 28 processor agreements, records of processing, DPIA, Art. 32 security/TOMs, 72-hour breach notification, third-country transfers, DPO, and the compliance-check checklist. |
| **DeepInfra & DSGVO** | `references/deepinfra-dsgvo.md` | Vendor-specific assessment: whether/how DeepInfra-hosted models can be used DSGVO-compliantly (US-only hosting = third-country transfer, AVV + SCC + TIA needed, the Google/Anthropic upstream sub-processor chain, PII-minimization at the source). Companion to the general `dsgvo` leaf when DeepInfra is the model host. |
| **Accessibility (a11y)** | `references/accessibility-a11y.md` | Web accessibility compliance: the EAA (Directive 2019/882) / Web Accessibility Directive / Austrian Barrierefreiheitsgesetz frame, WCAG 2.1 AA conformance target, the best-practice checklist (semantic HTML, ARIA, contrast, focus, keyboard, images, responsive, testing), an audit workflow, and field-tested fix recipes for legacy and CMS-exported static sites. |

## Routing

- **AI feature, risk tier, "is our AI high-risk", Article 50 / AI disclosure in consent or ToS**
  → read `references/eu-ai-act.md`.
- **Personal data, privacy notice / Datenschutzerklärung, lawful basis, data-subject rights,
  processor / AVV, DPIA, breach, third-country transfer, "check for DSGVO / GDPR compliance"**
  → read `references/dsgvo.md`.
- **A feature that uses AI on personal data** (LLM extraction, a chat assistant over user data,
  AI drafting about a person) → **both** leaves. Classify the AI use in the AI Act leaf, run the
  personal-data check in the DSGVO leaf, and keep the two disclosures consistent (Art. 50 AI
  notice and the DSGVO privacy notice must not contradict each other; name the human-review
  invariant once, it satisfies both the AI Act high-risk carve-out and DSGVO Art. 22).
- **DeepInfra is the model host** (DSGVO question about that specific vendor: US hosting, AVV,
  data-privacy-framework status, sub-processor chain) → read `references/deepinfra-dsgvo.md`
  alongside `references/dsgvo.md`.
- **Accessibility / a11y / WCAG / EAA / Barrierefreiheit** ("check accessibility", "a11y audit",
  "is this site accessible", "fix accessibility findings", shipping a customer-facing site)
  → read `references/accessibility-a11y.md`. This leaf is independent of the personal-data and
  AI leaves; run it on its own for an accessibility pass.

## Shared conventions (apply to every leaf and every deliverable)

- **Not legal advice.** Everything this skill produces is engineering-team orientation, not a
  legal opinion. Every document it helps author must say so and must recommend counsel (or the
  DPO) sign-off before any external compliance claim.
- **Two audiences, two checklists.** Both leaves produce a plain-language **stakeholder**
  checklist and a shorter decision-framed **owner / sign-off** checklist; keep the owner version
  to roughly a third the length.
- **These are live regulations.** Re-fetch the source pages before relying on specific dates,
  thresholds, or article numbers; do not trust cached dates, including any in these files.
- **Writing style: no em dashes.** Use a colon before a list or elaboration, parentheses or
  commas for an aside, a semicolon or two sentences for related clauses, and a comma or its own
  sentence for a hard qualifier ("only", "unless", "not"). Applies to every deliverable and to
  these files themselves.

## Sharing this skill with another project or machine

Zip the whole `compliance` folder (it carries both leaves):

- **Windows (PowerShell):** `Compress-Archive -Path ".claude\skills\compliance\*" -DestinationPath "compliance-skill.zip"`
- **macOS/Linux:** `zip -r compliance-skill.zip .claude/skills/compliance`

The recipient extracts to their repo's `.claude/skills/compliance/` (team-shared, commit it) or
their personal `~/.claude/skills/compliance/` (global). Keep the folder name `compliance` so it
matches the `name:` in this frontmatter. If a same-named skill already exists, reconcile rather
than blindly overwrite (read both, keep the better version of each file).
