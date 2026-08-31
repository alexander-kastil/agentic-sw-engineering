# EU AI Act (leaf of the `compliance` skill): Assessment & Disclosure Pattern

Leaf of the `compliance` master skill. Covers the AI-specific regulation; for the personal-data
regulation that almost always applies alongside it, see the sibling leaf [[dsgvo]]
(`references/dsgvo.md`). When an AI feature processes personal data, both leaves are in scope:
run the AI Act classification here, and run the DSGVO check in the sibling leaf.

Project-agnostic playbook for figuring out whether a product's AI use is regulated under the
EU AI Act, disclosing it correctly in user-facing consent/ToS text, and producing the two
kinds of write-ups stakeholders actually need: a plain-language checklist for a business
stakeholder, and a shorter sign-off checklist for the owner/decision-maker.

Source of truth: [artificialintelligenceact.eu](https://artificialintelligenceact.eu/) (also see
its [High-level Summary](https://artificialintelligenceact.eu/high-level-summary/),
[Small Businesses' Guide](https://artificialintelligenceact.eu/small-businesses-guide-to-the-ai-act/),
[Article 50 transparency guide](https://artificialintelligenceact.eu/transparency-rules-article-50/),
and [Compliance Checker](https://artificialintelligenceact.eu/assessment/eu-ai-act-compliance-checker/)).
**Re-fetch these before relying on specific dates or thresholds.** This is live EU legislation
in a phased rollout, and deadlines are actively being renegotiated (see the "Digital Omnibus"
update in Section 4 below, agreed May 2026 and formally endorsed by Parliament and Council in
June 2026); don't trust a cached date, including the ones in this file, without a quick re-check.

> **Common misconception to correct proactively:** "the AI Act got a grace period until
> December [2026]" is a real but *narrow* fact: it applies only to the Art. 50(2)
> machine-readable-marking sub-duty for legacy generative-AI systems, not to the core Art. 50
> disclosure duty (informing users they're talking to AI / that content is AI-generated), which
> is unaffected and still applies from 2 August 2026. If someone raises "isn't there a grace
> period" while you're drafting a disclosure clause or a checklist, this is almost certainly
> what they mean; confirm which of the two they're asking about before answering, and correct
> the scope rather than just agreeing.

## When to use

- A feature is being added that uses an LLM/AI to read, extract, summarize, or generate
  content involving personal data, or that a user talks to directly (chat assistant).
- Someone asks "is this AI Act compliant", "what risk tier is our AI feature", or "do we need
  to disclose AI use here".
- A consent screen, privacy notice, or Terms of Service needs an AI-disclosure clause.
- A non-technical stakeholder or the product owner needs a checklist to sign off on AI use.

## 1. Classify the AI use first (don't skip this)

Every other step depends on which tier the AI feature falls into. Walk this decision in order;
stop at the first tier that matches:

| Tier | Definition | Triggers |
| --- | --- | --- |
| **Prohibited (Art. 5)** | Banned outright | Manipulative/deceptive techniques, exploiting vulnerabilities, unauthorized biometric categorization, social scoring, predictive-policing profiling, facial-recognition-database scraping, workplace/education emotion inference, real-time public biometric ID (narrow law-enforcement exceptions) |
| **High-risk (Chapter III / Annex III)** | Heavy provider obligations: risk management, data governance, technical documentation, human-oversight design, accuracy/robustness | Safety component of an EU-regulated product, OR a listed Annex III use case (biometrics, critical infrastructure, education, **employment**, **credit/essential-services eligibility**, law enforcement, migration, justice), **unless** the AI only does narrow procedural tasks, improves prior human work, detects pattern deviations, or does preparatory work for a human decision |
| **Limited-risk / transparency (Art. 50)** | Must disclose AI involvement to the end user | Chatbots / conversational assistants; AI-generated or AI-modified content (text, audio, image, video); deepfakes |
| **Minimal risk** | Unregulated | Everything else (e.g. spam filters, most internal tooling) |
| **GPAI models** | Provider-side obligations (documentation, copyright, training-data summaries; extra obligations above 10^25 FLOPs "systemic risk") | Applies to whoever trains/publishes the underlying model: a downstream app that calls a hosted model (OpenAI, Anthropic, DeepSeek, etc.) is a *deployer*, not the GPAI provider |

**The two questions that usually settle it for a typical business app:**

1. **Does the AI decide something about a person with legal or similarly significant effect**
   (hiring, credit, benefits eligibility, biometric ID), autonomously? If no, you're very
   likely not high-risk, even if the *category* sounds high-risk, because of the
   "preparatory activity" / "human always reviews before it counts" carve-out.
2. **Does a human review and confirm the AI's output before it's ever acted on or stored**?
   If yes, and consistently enforced as a product invariant (not just a UI affordance a user
   can skip), that's strong evidence for the high-risk carve-out and should be named
   explicitly in the classification writeup.

If the AI only extracts/summarizes data for a human to review, or only powers a chat
assistant/proposal generator with no autonomous effect on a person, you're almost always in
**limited-risk / transparency (Art. 50)**, sometimes dropping to **minimal risk** if there's no
end-user-facing chat/generated-content surface at all. Document the reasoning, not just the
conclusion: a reviewer (or auditor) needs to see *why*, not just the label.

## 2. Article 50 transparency: the disclosure pattern for consent/ToS UI

**Deadline: Article 50 transparency obligations apply from 2 August 2026.** If that date is
still in the future when you're reading this, treat it as the one hard deadline worth calendar-
tracking; re-verify against the source site since implementation guidance may still shift.

The obligation is simple: **tell the end user when they're interacting with an AI system or
AI-generated/-assisted content.** The failure mode to avoid is *over*-disclosing: burying the
essential consent ask under a wall of legal/AI text hurts the exact usability the consent flow
exists to serve. Use a two-tier pattern:

- **Always-visible (essential only):** one short, factual sentence covering what data is
  captured, that AI assists the capture, and that a human reviews/confirms it before anything
  is stored or acted on. No legal-definition paragraphs, no hedging.
- **"Weitere Informationen" / "Further information" (collapsed by default):** the fuller
  detail, meaning the formal data-processing legal text (e.g. a GDPR Art. 4 processing
  definition), a fuller explanation of what the AI does and doesn't do (extraction only, never
  an autonomous decision about the person), and any outbound links (privacy policy, imprint).

Implementation: a native `<details>`/`<summary>` element is normally sufficient. Don't build a
bespoke accordion component just for this. Example shape (adapt wording/language to the product):

```html
<div class="card">
  <p><!-- essential purpose + data categories --></p>
  <p>
    <!-- one sentence: some data was captured with AI assistance; a human always
         reviews it before it's used/stored. -->
  </p>
  <details class="text-sm">
    <summary>Weitere Informationen</summary>
    <div>
      <p><!-- full legal processing-definition text --></p>
      <p>
        <!-- AI is used only for <data extraction / drafting / X>; it never makes an
             automated decision about you; a human reviews and confirms every result
             before it is acted on. -->
      </p>
    </div>
  </details>
  <!-- consent checkbox + confirm action, unchanged -->
</div>
```

Apply the same pattern to a **Terms of Service** clause if the product has one: a short
AI-use clause in the main body ("we use AI-assisted tools to help process X; a human reviews
outputs before Y"), with any fuller carve-outs/definitions in a linked/expandable section rather
than inline in the primary flow.

Keep the consent/ToS mechanism itself (checkbox, accept button, form binding) untouched. This
is a copy/markup change, never a logic change.

## 3. Two different checklists, two different audiences

Don't conflate these; they read very differently and go to different people.

### A. Stakeholder checklist (a business/product stakeholder, non-technical, non-legal)

Plain language, no jargon left unexplained, short paragraphs, action-oriented. Structure:

1. **Worum geht es? / What's this about?** One paragraph: what the law regulates, why it's
   relevant to *this* product specifically (name the actual AI-touching features).
2. **Einstufung / Classification.** Plainly state the risk tier and why, referencing the
   Annex III carve-outs and the human-review invariant from Step 1 above.
3. **Checkliste.** A literal `- [ ]` checklist of concrete, verifiable items (AI is labeled
   as AI in the UI; human review stays mandatory; consent/ToS discloses AI-assisted capture;
   no sensitive use cases in scope; note which model/provider powers which feature; the next
   hard deadline).
4. **Zeitplan / Timeline.** A small table of the dates that matter, explicitly marking which
   ones apply to this product and which don't.
5. **Offene Punkte / Open items.** Anything still undecided, and the trigger condition that
   would force re-classification (e.g. "if AI starts making decisions about our own staff's
   employment, this whole assessment must be redone").
6. **Not legal advice disclaimer.** Always include one; recommend counsel sign-off before any
   external compliance claim is made.
7. **Sources.** Link back to artificialintelligenceact.eu and the specific sub-pages used.

### B. Owner checklist (the person who must sign off / bears the decision)

Shorter, decision-and-risk-framed, not educational. Structure:

1. **Bottom line.** One or two sentences: are we compliant-by-design today, yes/no, and why
   (cite the human-review invariant and the "not high-risk" reasoning in one line each).
2. **Sign-off checklist.** A short `- [ ]` list of the things that actually need an owner
   decision or signature, not background reading: approve the Art. 50 disclosure wording;
   approve/reject going beyond the legal minimum on disclosure; confirm no plan exists to
   expand AI into an Annex III area (employment/credit/essential-services decisions about
   real people) without revisiting this assessment; confirm counsel has reviewed before any
   public compliance claim.
3. **Risk if we do nothing.** One paragraph, plain terms: what's the actual exposure if the
   Art. 50 deadline passes without action (reputational/regulatory, not overstated).
4. **Next hard date.** A single line, not a table: the one deadline that matters and how far
   away it is.
5. **Not legal advice disclaimer.**

Keep the owner version to roughly a third the length of the stakeholder version; its job is to
get a decision, not to teach the subject.

## 4. Timeline reference (verify before relying on these; this table was already revised once, see below)

| Date | What happens | Typically relevant to a downstream app? |
| --- | --- | --- |
| Feb 2025 | Prohibited practices (Art. 5) already in force | Only if you might be doing something on the prohibited list, usually "no, nothing to do" |
| Aug 2025 | GPAI model-provider obligations already in force | Applies to the model provider (OpenAI/Anthropic/DeepSeek/etc.), not a downstream deployer |
| **2 Aug 2026** | **Article 50 core disclosure duty takes effect**: inform users they're interacting with AI / that content is AI-generated. **Not delayed** by the Digital Omnibus. | **Yes, the deadline that matters for most chat/AI-extraction features** |
| 2 Dec 2026 | Digital Omnibus grace period for the Art. 50(2) machine-readable-marking/watermarking sub-duty, **only** for generative-AI systems already on the market before 2 Aug 2026; systems launched on/after that date get no grace | Usually **not** relevant to an internal chat/extraction tool: this matters for public-facing synthetic media (deepfakes, generated audio/image/video/text distributed to the public), not for a staff-facing assistant or a document-extraction draft a human reviews |
| 2 Dec 2027 | High-risk Annex III (stand-alone) deadline, **postponed from 2 Aug 2026** by the Digital Omnibus (political agreement 7 May 2026; formally endorsed by the European Parliament 16 Jun 2026 and the Council 29 Jun 2026) | Only if classification in Step 1 actually lands you in high-risk |
| 2 Aug 2028 | High-risk Annex I (safety component of a regulated product) deadline, **postponed from 2 Aug 2027** | Only if high-risk via the Annex I (regulated-product) pathway |

The Digital Omnibus also proposed a new Art. 5 prohibited-practice category (AI systems that
generate/manipulate non-consensual intimate imagery or CSAM); check the source site for its
final adopted wording if a feature could plausibly touch that area. It's a new addition, not a
loosening.

## 5. Not legal advice

Everything this skill produces is engineering-team orientation, not a legal opinion. Any
document it helps author should say so explicitly, and "get counsel to confirm before an
external compliance claim" language should carry through to both checklist types.

## 6. Sharing this skill with another project or machine

This leaf ships as part of the `compliance` skill. The clean way to hand it to a project that
isn't reachable for a direct local/global sync (a different machine, a project you don't have
open) is a zip of the whole `compliance` skill folder (which carries both this leaf and the
[[dsgvo]] leaf):

- **Windows (PowerShell):** `Compress-Archive -Path ".claude\skills\compliance\*" -DestinationPath "compliance-skill.zip"`
- **macOS/Linux:** `zip -r compliance-skill.zip .claude/skills/compliance`

The recipient extracts it to their own repo's `.claude/skills/compliance/` (team-shared, commit
it) or their personal `~/.claude/skills/compliance/` (global, cross-project), keeping the folder
name `compliance` so it matches the `name:` field in the master `SKILL.md` frontmatter. If the
recipient already has a same-named skill, treat the zip like any local-vs-global copy and
reconcile rather than blindly overwrite (read both, keep the better version of each file).

## 7. Writing style for anything this skill produces

Whatever this skill outputs (checklists, skill/doc prose, consent copy, artifacts) avoids em
dashes (—). Pick the punctuation the sentence actually needs instead:

- Introducing an elaboration or a list: use a colon.
- A parenthetical aside: use parentheses or commas.
- Two independent but related clauses: use a semicolon, or split into two sentences.
- A hard qualifier ("only", "unless", "not"): use a comma or its own sentence, not a dash.

This applies to every deliverable this skill produces, including this file itself: if you're
editing it and reach for an em dash, use one of the above instead.
