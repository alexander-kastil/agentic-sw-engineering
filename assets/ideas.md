# Ideas

Captured input worth turning into class material. One section per source.

## VS Code release: Claude sessions and live preview (Aug 2026)

Source: [@code thread, 12 Aug 2026](https://x.com/code/status/2087591365357998136), 6 posts by the author, captured 13 Aug 2026.

Five shipped features from the latest VS Code release:

1. **Model switching inside one Claude session.** The picker offers Anthropic models (Default, Fable, Sonnet) and Copilot-provided ones (Claude Haiku 4.5, Opus 4.7, Sonnet 5) side by side, and the choice applies per turn rather than per session. BYOK and Copilot subscription models are selectable from the same list.
2. **Claude in the Agents window without a GitHub sign-in.** Experimental, opt-in through a setting that skips the sign-in prompt.
3. **Auto-reload for local HTML previews.** The preview refreshes when the file changes on disk, toggleable per tab or set as the default.
4. **Sticky scroll in chat.** The prompt stays pinned at the top while scrolling its response, so a long answer stays attached to the question that produced it.
5. Full release notes linked from the thread's last post.

### Why it is relevant to the class

- **Module 3 (agentic-coding), `05-claude-code/`:** per-turn model switching is a concrete teaching moment for cost and capability tiering. Cheap model for mechanical turns, strong model for the hard turn, in one conversation and without losing context. That is the same tiering idea the orchestration content argues for, now visible in the editor UI.
- **Module 2 (copilot-tools):** the shared picker is evidence for how the BYOK versus subscription boundary actually presents to a developer, rather than as an abstract licensing discussion.
- **Demo hygiene:** auto-reload for local HTML previews removes a manual refresh step from any demo that renders a generated page.
- Screenshots for slides are in the thread's posts if the release notes lack equivalents.

### Open question

Whether per-turn switching preserves prompt caching across a model change, since a switch mid-session would plausibly invalidate the cache and change the cost story before it gets taught.
