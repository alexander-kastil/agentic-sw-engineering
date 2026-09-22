---
name: learn-docs-lookup
description: Answer a question about a Microsoft or Azure product from the official documentation instead of from memory, using the microsoft-learn MCP server. Use whenever a question names an Azure service, a .NET API, Microsoft Entra, Microsoft Foundry, or any learn.microsoft.com topic, and always before stating a version number, a quota, a pricing tier, or a product availability fact.
---

# Learn Docs Lookup

A product fact stated from memory is a guess with a citation-shaped hole in it. This skill routes the answer through the official documentation and makes the source visible.

## When this fires

Any question naming a Microsoft or Azure product, and any claim about a version, a limit, a tier, a region, or whether a feature exists.

## How to answer

1. Search the documentation with the `microsoft_docs_search` tool from the `microsoft-learn` server.
2. When the excerpt is too thin to answer from, fetch the full page with `microsoft_docs_fetch`.
3. Answer in at most five sentences, then list every page you used as a Markdown link.

## Rules

| Rule | Why |
|------|-----|
| Never answer a version, quota, tier, or availability question without a search | These are the facts that rot fastest, and they are the ones a reader acts on. |
| Cite every page you used | An uncited answer cannot be checked, and an answer that cannot be checked is worth no more than a guess. |
| Say "not found in the documentation" rather than filling the gap | A missing page is a real answer. An invented one costs the reader a debugging session. |
| Prefer the product documentation over a changelog | A changelog reports deltas; only the documentation reports the current model. |
