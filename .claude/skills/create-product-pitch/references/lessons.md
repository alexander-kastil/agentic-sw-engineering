# Lessons learned. Create-product-pitch pipeline

Distilled gotchas from prior runs. Update whenever a run produces a new lesson.

## 1. Gamma `additionalInstructions` has a hard 5000-character limit

Returns HTTP 400 if exceeded. Trim aggressively before sending. Practical structure: keep per-slide image direction to 1–2 sentences, drop decorative wording, omit content already in `inputText`.

The slide-prompt file authored by [[pitch-slides]] should include both a verbose human-readable section AND a terse "ADDITIONAL INSTRUCTIONS BLOCK" at the end. [[pitch-gamma]] sends only the terse block.

## 2. Image style is best-effort, not contractual

`imageOptions.stylePreset: "photorealistic"` can be overridden by Gamma's chosen theme. In one run, every "photorealistic" image came back as "Modern vector illustration" because the theme applied an `artStylePreset: "illustration"`. Composition and subject were correct; rendering style was theme-driven.

Mitigation: pre-select a known photorealistic theme via `get_themes` before generating, OR accept the override and surface it to the user.

## 3. "No people" must be repeated per slide

Stating "no people in any image" once at the top of `additionalInstructions` is not reliable. State it again in EVERY per-slide image direction. Even then, Gamma is best-effort; a person occasionally slips through. The user iterates in the Gamma editor; do not re-generate.

## 4. PowerPoint COM `MsoTriState` enum fails to resolve

```powershell
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
# → Unable to find type [Microsoft.Office.Core.MsoTriState]
```

Use the numeric value:

```powershell
$ppt.Visible = -1  # msoTrue
```

PowerPoint COM also refuses to operate truly invisible. `$true` and `$false` both fail in different ways. `-1` is correct.

## 5. Headless export tools are usually absent on Windows

`soffice`, `libreoffice`, `pdftoppm`, ImageMagick are typically NOT installed on Windows dev machines. `convert.exe` resolves to Windows' built-in filesystem conversion utility, not ImageMagick. Probe before promising.

PowerPoint COM IS reliably available on Office 365 machines.

## 6. Do not poll guessed Gamma API URLs

The Bash auto-mode classifier (rightly) blocks polling `https://gamma.app/api/generations/...` in a loop — the URL is agent-guessed and could hammer the service. Use `mcp__claude_ai_Gamma__get_generation_status` instead. Single calls are fine; tight loops are not.

## 7. Generation takes 1–3 minutes; the widget polls; you should not

The interactive widget rendered by `generate` polls completion automatically. The Claude session does not need to poll. To retrieve the `exportUrl` for download, call `get_generation_status` once after ~75 seconds. If still pending, wait a similar interval and check once more.

`ScheduleWakeup` is for `/loop` dynamic mode only and is not applicable here.

## 8. Em dashes must be removed BEFORE the Gamma call

The NRE brand voice rule (no em dashes) was caught mid-flight in one run. The Gamma call had already been triggered with em-dash-laden text. Cost: ~35 wasted credits plus a re-run.

[[pitch-brand-voice]] is the stage gate. `grep -c "—"` must return 0 on both pitch files before [[pitch-gamma]] runs.

## 9. Project-specific voice rules live in memory

Always read `MEMORY.md` and `feedback_*.md` entries before scrubbing. Each project may have additional rules (no superlatives, no AI tell-words, mandatory phrases). The em-dash rule is the default; project rules layer on top.

## 10. Gamma export is single-format per call

`exportAs` accepts one of `pptx` or `pdf`, not both. For dual delivery, run [[pitch-export]] off the PPTX and have the user export PDF from the Gamma editor. Do not call `generate` twice — that's another 30+ credits.

## 11. The `inputText` outline is what drives slide content

Gamma uses `inputText` with `textMode: generate` to author the slide bodies. `additionalInstructions` shapes structure and visuals but does NOT replace the source text. If `inputText` is shallow, no amount of `additionalInstructions` rescues the result.

## 14. PowerPoint COM `Presentations.Add()` can return 0 slides

On some PowerPoint versions, `Presentations.Add()` creates a presentation with 0 slides instead of 1 blank. Assuming there is a blank to delete after inserts can silently delete a real inserted slide (we lost the closing tiers slide once this way).

**Mitigation:** the [[pitch-bundle]] algorithm now opens an existing source PPTX as the base and inserts the new slides into it. No blank to manage, theme inherits cleanly.

## 15. The 'open-base' bundle pattern preserves theme without re-running Gamma

After adding several slides to a deck via [[pitch-add-slide]], the canonical bundled `.pptx` is refreshed via [[pitch-bundle]] which opens the original full-deck PPTX as the base and inserts only the new single-slide PPTXs at the right positions. Cost: zero credits, ~10 seconds wall time. Compare to re-running Gamma Pattern A on the entire deck: ~30+ credits.

## 16. "No sunk cost" — keep both renders when a correction lands mid-flight

When a Gamma call has already fired and a correction comes in (different layout, different angle), the first render is paid for and is real work. Find a narrative slot for it instead of discarding. The pillars/hero split on slides 08 and 09 of the Mini AI Server deck came from exactly this situation. See [[feedback-no-sunk-cost]] in project memory.

## 12. Frontmatter is the source of truth, not the image

The canonical order is **prompt → frontmatter → slide/image**, not the reverse. Each slide's `.md` frontmatter (with `gamma_prompt`, `visual-prompt`, `content` bullets, speaker notes) is the spec; the PNG is generated FROM the frontmatter, never before it. Generating first and back-filling the `.md` is brittle and bypasses brand-voice scrub. When adding a slide late to an existing deck, write the `.md` first, scrub, then trigger Gamma. See [[pitch-slides]] for the schema and [[pitch-gamma]] for how it reads the frontmatter.

## 13. Match the existing reference deck's rhythm

When a sibling product already has a Gamma deck, read 1–2 slides of it during [[pitch-sources]] and mirror the section rhythm. Customers should feel the two decks come from one product family. This is one reason the master skill defaults to the Problem → Lösung → Anwendung → Nächste Schritte structure inherited from the NRE mail-automation deck.
