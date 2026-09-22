# agentic-seo-audit-technical

Run a stricter technical SEO audit against the local preview.

This is the runtime-focused audit. It should verify what the browser actually renders on representative local routes and capture issues that code inspection alone can miss: rendered metadata, JSON-LD output, Lighthouse failures, shared CTA defects, contrast problems, accessible-name mismatches, and other template-level regressions.

## BLOCKING: Do NOT Read `.seo/` Until Audit Is Complete

**The `.seo/` directory is off-limits during audit execution.** Do NOT list, read, search, or inspect any file under `.seo/` until AFTER every audit section is written and all scores are assigned. Reason: prior audit findings contaminate the fresh snapshot. The only time `.seo/` is touched is during the Baseline-Finding Algorithm (after scoring), comparison file generation (after scoring), and the Runs Log update (after writing).

## BLOCKING: No Baseline in Audit Body

**Every run is a fresh independent snapshot.** The baseline only exists at the very end — in the auto-generated `SEO_AUDIT-TECHNICAL-comparrison.md` file — and only as a numeric comparison. Violations:

- Do NOT label findings as "Persists", "New finding", "Improved", or "Resolved (by architecture)"
- Do NOT mention a previous audit, baseline date, or prior score in the header, Executive Summary, or any audit section
- Do NOT reference "the last audit", "previous run", or a prior date anywhere in the body
- State every finding on its own merits as if this is the FIRST audit ever run
- Only invoke the Baseline-Finding Algorithm AFTER all sections are written and scored

## BLOCKING: Audit Only Public Crawl Surface

- Build the audited route set from `robots.txt`, `sitemap.xml`, visible navigation, and public links discovered from those pages.
- Do not force-check guessed routes or hidden collection URLs unless they are exposed in public runtime output or explicitly named by the user.
- Do not create findings from hidden CMS structure, configuration internals, build manifests, or checked-in generated output unless they leak into public runtime output.
- Use code inspection only to confirm the root cause of a public runtime defect.
- Do not score local preview host/port mismatches as SEO defects. They are local audit-environment notes unless the same mismatch exists on a public deployment or the user explicitly asks to debug the local setup.

## Local-First Execution Policy

- Audit the local preview or another local/dev URL by default.
- Reuse an existing local browser session if one is already running.
- Do not start a new preview process when the user has already provided a running app.
- Prefer browser/runtime inspection over terminal-driven discovery.
- Do not open or inspect production URLs unless the user explicitly asks for production testing.
- If the local preview is unavailable, limit the audit to public artifacts the user explicitly provided and clearly note that runtime verification could not be completed.

## Triggers

"technical seo audit", "local seo audit", "runtime seo audit", "lighthouse seo audit", "chrome devtools seo"

## When to Use

- Validate a local optimization sprint before or after code changes
- Check rendered titles, descriptions, canonicals, links, headings, JSON-LD, and images on key routes
- Confirm whether a fix actually landed in runtime output
- Produce a technical-only series that can be compared without mixing in broader strategic audits

## Preferred Audit Inputs

1. Local preview URL, for example `http://localhost:1313/` or `http://localhost:4200/`
2. Browser checks on `robots.txt`, `sitemap.xml`, visible navigation, and representative public routes discovered from those sources
3. Local code inspection for root-cause confirmation when a runtime defect appears

## Audit Output Convention

Technical audits use the `TECHNICAL` series:

```
.seo/YYYY-MM-DD/SEO_AUDIT-TECHNICAL-hhmm.md         ← runtime audit snapshot
.seo/YYYY-MM-DD/SEO_AUDIT-TECHNICAL-comparrison.md  ← latest technical comparison
.seo/readme.md                                      ← runs log + type-specific charts
```

## Baseline-Finding Algorithm

1. List `.seo/{today}/` and find `SEO_AUDIT-TECHNICAL-*.md`
2. Sort by `hhmm` descending and use the latest same-type run as baseline
3. If no same-type file exists today, scan earlier date folders for the latest `SEO_AUDIT-TECHNICAL-*.md`
4. If no typed technical baseline exists yet, mark the run as the first technical snapshot instead of comparing it to a general audit
5. Write the new audit as `SEO_AUDIT-TECHNICAL-{current hhmm}.md`
6. Auto-generate or update `SEO_AUDIT-TECHNICAL-comparrison.md`
7. Append a `Technical` row in `.seo/readme.md` and update only the technical chart

## Runs Log

Append to `.seo/readme.md` under `## SEO Runs` with newest rows first:

| Date | Time | Type | Score | Technical SEO | On-Page SEO | Content Quality | Authority |

Only update the technical progression chart when this skill writes a new run.

## Verification Notes

- Prefer browser inspection over raw HTML fetches for schema and rendered metadata.
- Do not turn local preview host/port differences into SEO findings or score deltas unless the same issue is visible on a public deployment.
- `web_fetch` and `curl` cannot reliably detect runtime JSON-LD. Verify with:

```js
document.querySelectorAll('script[type="application/ld+json"]')
```

- Treat Lighthouse issues as runtime evidence, then confirm the root cause in templates or CSS before prescribing fixes.

## Audit Priority Order

1. Crawlability and rendered metadata on public routes discovered from nav, sitemap, and robots
2. Canonicals, schema output, and structured-data correctness on those public routes
3. Lighthouse SEO, accessibility, and best-practices failures caused by shared templates on public pages
4. CTA text quality, contrast, accessible names, and other repeated UI defects visible on public pages
5. Re-run guidance for confirming the next local plateau
