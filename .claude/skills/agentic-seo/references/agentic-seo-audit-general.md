# agentic-seo-audit-general

Run a broader SEO health audit across a web project.

This is the code-first and strategy-oriented audit. It should answer the bigger SEO question: how healthy is the site overall, what moved since the last broad review, and what should be fixed next across technical foundations, on-page SEO, content quality, and authority.

## BLOCKING: Do NOT Read `.seo/` Until Audit Is Complete

**The `.seo/` directory is off-limits during audit execution.** Do NOT list, read, search, or inspect any file under `.seo/` until AFTER every audit section is written and all scores are assigned. Reason: prior audit findings contaminate the fresh snapshot. The only time `.seo/` is touched is during the Baseline-Finding Algorithm (after scoring) and the Runs Log update (after writing).

## BLOCKING: No Baseline in Audit Body

**Every run is a fresh independent snapshot.** The baseline only exists at the very end — in the Score Delta section — and only as a scores-only numeric table. Violations:

- Do NOT write a "Net Change Since" section in the Executive Summary
- Do NOT label findings as "Persists", "New finding", "Improved", or "Resolved (by architecture)"
- Do NOT mention a previous audit, baseline date, or prior score in the header, Executive Summary, or any audit section
- Do NOT write a "Baseline:" line in the audit header
- Do NOT reference "the last audit", "previous run", or "since March" anywhere in the body
- State every finding on its own merits as if this is the FIRST audit ever run
- Only invoke the Baseline-Finding Algorithm AFTER all sections are written and scored

## BLOCKING: Audit Only Public Crawl Surface

- Score only what a crawler can discover from `robots.txt`, `sitemap.xml`, visible navigation, and public links reachable from those entry points.
- Do not create findings from hidden CMS sections, front matter, configuration internals, build manifests, or checked-in generated output unless they leak into public runtime output.
- Do not force-check guessed routes or non-public collection URLs unless they appear in the nav, sitemap, public HTML, or the user explicitly asks for them.
- Use code inspection only after a public issue is visible. Do not use internal structure as audit evidence by itself.
- Do not score local preview host/port differences as SEO defects. They are audit-environment notes unless reproduced on a public target or the user explicitly asks to debug the local setup.

## Local-First Execution Policy

- Use the local preview or another local/dev URL first when page examples are needed.
- Reuse the user's existing local app and browser session when one already exists.
- Prefer browser/runtime inspection over broad repository inspection.
- Do not inspect production URLs unless the user explicitly asks for production validation.
- If the local preview is unavailable, limit the audit to public artifacts the user explicitly provided and clearly call out the missing runtime checks.

## Triggers

"general seo audit", "seo health review", "overall seo audit", "seo roadmap", "why am i not ranking"

## When to Use

- Produce a broad SEO snapshot for the whole site
- Review titles, descriptions, heading structure, canonical setup, schema coverage, content quality, and authority signals
- Summarize progress across audits at an executive level
- Build or refresh a prioritized SEO backlog

## Preferred Audit Inputs

1. Local preview and existing browser session for representative spot checks
2. `robots.txt`, `sitemap.xml`, visible navigation, and public links discovered from those entry points
3. Targeted code inspection only for root-cause confirmation after a public defect appears
4. Existing `.seo/` snapshots are read **only for previous scores** — never to frame findings

## Audit Execution Order

Run the full independent audit in this order before touching any baseline or comparison data:

1. Crawlability and indexation
2. Technical foundations and schema coverage on public URLs discovered from the crawl surface
3. On-page optimization (titles, descriptions, heading structure, canonicals, OG) on public pages
4. Content quality and internal linking visible on public pages
5. Authority, trust signals, and off-site gaps visible to crawlers

**State every finding on its own merits.** Do not frame findings as "persists since X", "new since X", or "carried forward from". Each finding stands alone.

After all sections are written and scores are assigned, invoke the Baseline-Finding Algorithm.

## Audit Output Convention

General audits use the `GENERAL` series:

```
.seo/YYYY-MM-DD/SEO_AUDIT-GENERAL-hhmm.md  ← full independent audit snapshot
.seo/readme.md                              ← runs log + type-specific charts
```

`hhmm` is the 24-hour zero-padded run time. Each run is a full independent snapshot.

The audit file structure is:

1. Header (date, time, scope, method) — NO baseline line
2. Executive Summary (overall score + one-paragraph assessment) — NO delta/vs comparisons
3. Technical SEO (sections 1.1–1.N)
4. On-Page SEO
5. Content Quality
6. Authority & Trust
7. Prioritized Backlog
8. Score Delta (scores only — see below; skip entirely if no prior baseline exists)

## Baseline-Finding Algorithm

Invoke **after** all audit sections and scores are complete.

1. List `.seo/{today}/` and find `SEO_AUDIT-GENERAL-*.md`
2. Sort by `hhmm` descending — use the latest same-type run as baseline
3. If no same-type file exists today, scan earlier date folders for the latest `SEO_AUDIT-GENERAL-*.md`
4. If no baseline exists, skip the Score Delta section entirely
5. Write the Score Delta section as a scores-only table appended at the end of the audit file:

```
## Score Delta vs {baseline date}

| Category | Previous | Current | Change |
|---|---|---|---|
| Overall | X.X/10 | X.X/10 | ▲/▼ |
| Technical SEO | ... | ... | ... |
| On-Page SEO | ... | ... | ... |
| Content Quality | ... | ... | ... |
| Authority | ... | ... | ... |
```

No narrative in the Score Delta section — numbers only.

## Runs Log

After writing the audit file:

1. Append a row to `.seo/readme.md` under `## General SEO Runs` (newest row first)
2. Update only the General Score Progression chart

| Date | Time | Score | Technical SEO | On-Page SEO | Content Quality | Authority |

Only update the general progression chart when this skill writes a new run.
