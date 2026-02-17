---
name: make-ebook
description: Builds a single PDF (and optional EPUB) from repo Markdown using Pandoc and uploads as a CI artifact. Use when generating documentation PDFs, creating ebook distributions, building PDF from markdown sources, or automating document distribution. Works with GitHub Actions workflow automation and supports custom ordering via .bookorder file.
---

## When to Use This Skill

Invoke this skill when you need to:

- Convert repository Markdown documentation into a single PDF ebook
- Generate EPUB files for ebook distribution
- Automate PDF builds in CI/CD with GitHub Actions
- Create ordered documentation from multiple markdown files
- Build downloadable documentation artifacts

## How It Works

When invoked:

1. Ensure `.github/workflows/ebook.yml` exists. If missing, create it from the project's README ordering and `docs/` tree.
2. In GitHub, trigger the `Build PDF ebook` workflow on the `main` branch (or current branch).
3. After completion, provide the artifact download link.

## Configuration Rules

- Use `docker://pandoc/latex:3.8` in GitHub Actions
- Default order: `README.md` first, then `docs/**/*.md` (sorted)
- Allow a `.bookorder` file to override default ordering
- Include Pandoc options: `--toc`, `--from=gfm`, `--pdf-engine=xelatex`
- Output file: `output/ebook.pdf`

## File Ordering

The skill respects document ordering in this priority:

1. Custom `.bookorder` file (if present)
2. Default: `README.md` + `docs/**/*.md` alphabetically sorted

Create `.bookorder` to customize the sequence:
