"""Unit tests for evaluate.py. Run with: pytest dashboard/test_evaluate.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest
from evaluate import (
    has_real_content,
    evaluate_theory,
    evaluate_demos,
    evaluate_labs,
    evaluate_slides,
    evaluate_module,
)


# ---------------------------------------------------------------------------
# has_real_content
# ---------------------------------------------------------------------------

def test_content_code_block(tmp_path):
    f = tmp_path / "readme.md"
    f.write_text("# Title\n\n```bash\necho hello\n```\n")
    assert has_real_content(f)


def test_content_prose(tmp_path):
    f = tmp_path / "readme.md"
    f.write_text("# Title\n\nThis is a prose paragraph that is definitely long enough.\n")
    assert has_real_content(f)


def test_content_bullet_only(tmp_path):
    f = tmp_path / "readme.md"
    f.write_text("# Title\n\n- item one\n- item two\n- item three\n")
    assert not has_real_content(f)


def test_content_headings_only(tmp_path):
    f = tmp_path / "readme.md"
    f.write_text("# Title\n\n## Subtitle\n\n### Sub-sub\n")
    assert not has_real_content(f)


def test_content_missing_file(tmp_path):
    assert not has_real_content(tmp_path / "nonexistent.md")


def test_content_short_line_ignored(tmp_path):
    f = tmp_path / "readme.md"
    f.write_text("# Title\n\nshort\n")
    assert not has_real_content(f)


# ---------------------------------------------------------------------------
# evaluate_theory
# ---------------------------------------------------------------------------

def test_theory_done(tmp_path):
    topic = tmp_path / "01-intro"
    topic.mkdir()
    (topic / "readme.md").write_text("# Intro\n\nThis is prose content that counts as theory.\n")
    assert evaluate_theory(tmp_path) == "done"


def test_theory_done_code_block(tmp_path):
    topic = tmp_path / "01-intro"
    topic.mkdir()
    (topic / "readme.md").write_text("# Intro\n\n```python\nprint('hello')\n```\n")
    assert evaluate_theory(tmp_path) == "done"


def test_theory_doing_empty_readme(tmp_path):
    topic = tmp_path / "01-intro"
    topic.mkdir()
    (topic / "readme.md").write_text("# Intro\n")
    assert evaluate_theory(tmp_path) == "doing"


def test_theory_doing_no_readmes(tmp_path):
    topic = tmp_path / "01-intro"
    topic.mkdir()
    assert evaluate_theory(tmp_path) == "doing"


def test_theory_planned_no_topics(tmp_path):
    assert evaluate_theory(tmp_path) == "planned"


def test_theory_planned_no_dir():
    assert evaluate_theory(Path("/nonexistent/path")) == "planned"


def test_theory_planned_none():
    assert evaluate_theory(None) == "planned"


def test_theory_non_numeric_dirs_ignored(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "_images").mkdir()
    assert evaluate_theory(tmp_path) == "planned"


# ---------------------------------------------------------------------------
# evaluate_demos
# ---------------------------------------------------------------------------

def test_demos_done_package_json(tmp_path):
    sub = tmp_path / "01-intro" / "my-app"
    sub.mkdir(parents=True)
    (sub / "package.json").write_text("{}")
    assert evaluate_demos(tmp_path) == "done"


def test_demos_done_csproj(tmp_path):
    sub = tmp_path / "01-intro" / "MyApp"
    sub.mkdir(parents=True)
    (sub / "MyApp.csproj").write_text("<Project/>")
    assert evaluate_demos(tmp_path) == "done"


def test_demos_done_requirements(tmp_path):
    sub = tmp_path / "app"
    sub.mkdir()
    (sub / "requirements.txt").write_text("requests\n")
    assert evaluate_demos(tmp_path) == "done"


def test_demos_done_subfolder(tmp_path):
    sub = tmp_path / "demos"
    sub.mkdir()
    (sub / "demo-01-intro.md").write_text("# Demo 01\n\nThis demo walks through a complete worked example.\n")
    assert evaluate_demos(tmp_path) == "done"


def test_demos_planned_no_projects(tmp_path):
    (tmp_path / "readme.md").write_text("# Module\n")
    assert evaluate_demos(tmp_path) == "planned"


def test_demos_planned_no_dir():
    assert evaluate_demos(Path("/nonexistent/path")) == "planned"


def test_demos_planned_none():
    assert evaluate_demos(None) == "planned"


# ---------------------------------------------------------------------------
# evaluate_labs
# ---------------------------------------------------------------------------

def test_labs_done_subfolder(tmp_path):
    lab = tmp_path / "01-my-lab"
    lab.mkdir()
    (lab / "readme.md").write_text("# My Lab\n\nThis lab walks you through building something useful.\n")
    assert evaluate_labs(tmp_path) == "done"


def test_labs_done_flat_file(tmp_path):
    f = tmp_path / "lab-01-intro.md"
    f.write_text("# Lab 01\n\nThis lab teaches you how to do something interesting.\n")
    assert evaluate_labs(tmp_path) == "done"


def test_labs_doing_empty_subfolder(tmp_path):
    lab = tmp_path / "01-my-lab"
    lab.mkdir()
    (lab / "readme.md").write_text("# My Lab\n")
    assert evaluate_labs(tmp_path) == "doing"


def test_labs_doing_dir_exists_no_content(tmp_path):
    assert evaluate_labs(tmp_path) == "doing"


def test_labs_planned_no_dir(tmp_path):
    assert evaluate_labs(tmp_path / "nonexistent") == "planned"


def test_labs_absent_no_labs_sentinel(tmp_path):
    (tmp_path / "readme.md").write_text("# Module Labs\n\nNo Labs for this Module.\n")
    assert evaluate_labs(tmp_path) == "absent"


def test_labs_ignores_non_numeric_subdirs(tmp_path):
    non_lab = tmp_path / "assets"
    non_lab.mkdir()
    (non_lab / "readme.md").write_text("# Assets\n\nThis is a very long prose line that might trick the check.\n")
    assert evaluate_labs(tmp_path) == "doing"


def test_labs_flat_file_wrong_pattern_ignored(tmp_path):
    f = tmp_path / "notes.md"
    f.write_text("# Notes\n\nThis is prose content that is long enough.\n")
    assert evaluate_labs(tmp_path) == "doing"


# ---------------------------------------------------------------------------
# evaluate_slides
# ---------------------------------------------------------------------------

def test_slides_done(tmp_path):
    pptx = tmp_path / "pptx"
    pptx.mkdir()
    (pptx / "module-01.pptx").write_bytes(b"fake")
    assert evaluate_slides(tmp_path) == "done"


def test_slides_doing_prep_specs(tmp_path):
    pptx = tmp_path / "pptx"
    pptx.mkdir()
    (pptx / "01-01-intro.md").write_text("# Slide 01\n\nThis slide spec describes the opening slide content in detail.\n")
    assert evaluate_slides(tmp_path) == "doing"


def test_slides_planned_placeholder_readme(tmp_path):
    pptx = tmp_path / "pptx"
    pptx.mkdir()
    (pptx / "readme.md").write_text("# Slides\n")
    assert evaluate_slides(tmp_path) == "planned"


def test_slides_planned_empty_pptx(tmp_path):
    (tmp_path / "pptx").mkdir()
    assert evaluate_slides(tmp_path) == "planned"


def test_slides_planned_no_pptx_dir(tmp_path):
    assert evaluate_slides(tmp_path) == "planned"


def test_slides_planned_no_dir():
    assert evaluate_slides(Path("/nonexistent/path")) == "planned"


def test_slides_planned_none():
    assert evaluate_slides(None) == "planned"


# ---------------------------------------------------------------------------
# evaluate_module (integration)
# ---------------------------------------------------------------------------

def test_evaluate_module_full(tmp_path):
    module_dir = tmp_path / "demos" / "01-intro"
    topic = module_dir / "01-basics"
    topic.mkdir(parents=True)
    (topic / "readme.md").write_text("# Basics\n\nThis is real prose content for the theory section.\n")

    app = module_dir / "01-basics" / "my-app"
    app.mkdir()
    (app / "package.json").write_text("{}")

    labs_dir = tmp_path / "labs" / "01-intro" / "01-lab"
    labs_dir.mkdir(parents=True)
    (labs_dir / "readme.md").write_text("# Lab 01\n\nThis lab walks you through a guided exercise.\n")

    m = {"num": "01", "name": "Intro", "path": "demos/01-intro"}
    result = evaluate_module(m, tmp_path)

    assert result["theory"] == "done"
    assert result["demos"] == "done"
    assert result["labs"] == "done"
    assert result["slides"] == "planned"
