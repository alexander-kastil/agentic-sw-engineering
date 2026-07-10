#!/usr/bin/env python3
"""Evaluate module completeness and write status fields into dashboard/dashboard.json."""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = Path(__file__).resolve().parent
DASHBOARD_PATH = DASHBOARD_DIR / "dashboard.json"

CODE_PROJECT_GLOBS = ["package.json", "*.csproj", "*.sln", "requirements.txt", "go.mod"]
LAB_FILE_RE = re.compile(r"^lab-\d+.*\.md$", re.IGNORECASE)
DEMO_FILE_RE = re.compile(r"^(?:\d{2}-demo-|demo-\d{2}-).*\.md$", re.IGNORECASE)


def has_real_content(path: Path) -> bool:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("```"):
                return True
            if s and not s.startswith(("#", "-", "*", ">", "|", "!")) and len(s) > 20:
                return True
    except Exception:
        pass
    return False


def evaluate_theory(module_dir: Path | None) -> str:
    if not module_dir or not module_dir.exists():
        return "planned"
    topics = [
        d for d in sorted(module_dir.iterdir())
        if d.is_dir() and len(d.name) >= 2 and d.name[:2].isdigit()
    ]
    if not topics:
        return "planned"
    for d in topics:
        readme = d / "readme.md"
        if readme.exists() and has_real_content(readme):
            return "done"
    return "doing"


def evaluate_demos(module_dir: Path | None) -> str:
    if not module_dir or not module_dir.exists():
        return "planned"
    for pattern in CODE_PROJECT_GLOBS:
        if list(module_dir.rglob(pattern)):
            return "done"
    scan_dirs = [module_dir]
    demos_sub = module_dir / "demos"
    if demos_sub.is_dir():
        scan_dirs.append(demos_sub)
    for d in scan_dirs:
        for f in d.iterdir():
            if f.is_file() and DEMO_FILE_RE.match(f.name) and has_real_content(f):
                return "done"
    return "planned"


def evaluate_labs(labs_dir: Path) -> str:
    if not labs_dir.exists():
        return "planned"
    for child in sorted(labs_dir.iterdir()):
        if child.is_dir() and len(child.name) >= 2 and child.name[:2].isdigit():
            for name in ("readme.md", "README.md"):
                readme = child / name
                if readme.exists() and has_real_content(readme):
                    return "done"
    for f in sorted(labs_dir.iterdir()):
        if f.is_file() and LAB_FILE_RE.match(f.name) and has_real_content(f):
            return "done"
    readme = labs_dir / "readme.md"
    if readme.exists() and "no lab" in readme.read_text(encoding="utf-8").lower():
        return "absent"
    return "doing"


def evaluate_slides(module_dir: Path | None) -> str:
    if not module_dir or not module_dir.exists():
        return "planned"
    pptx_dir = module_dir / "pptx"
    if not pptx_dir.exists():
        return "planned"
    if list(pptx_dir.glob("*.pptx")):
        return "done"
    for f in pptx_dir.iterdir():
        if f.is_file() and f.suffix.lower() == ".md" and f.name.lower() != "readme.md" and has_real_content(f):
            return "doing"
    return "planned"


def find_dir(repo_root: Path, num: str, subdir: str) -> Path | None:
    base = repo_root / subdir
    if not base.exists():
        return None
    for d in sorted(base.iterdir()):
        if d.is_dir() and d.name.startswith(f"{num}-"):
            return d
    return None


def read_module_name(module_dir: Path | None) -> str | None:
    if not module_dir:
        return None
    readme = module_dir / "readme.md"
    if not readme.exists():
        return None
    for line in readme.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# "):
            title = re.sub(r"^Module\s+\d+[:\-–]?\s*", "", line[2:]).strip()
            return title or None
    return None


def evaluate_module(m: dict, repo_root: Path) -> dict:
    num = m["num"]
    module_dir = find_dir(repo_root, num, "demos")
    labs_dir = find_dir(repo_root, num, "labs") or Path("/nonexistent")
    name = read_module_name(module_dir) or m["name"]
    return {
        "num": num,
        "name": name,
        "path": f"demos/{module_dir.name}" if module_dir else m.get("path", ""),
        "theory": evaluate_theory(module_dir),
        "demos": evaluate_demos(module_dir),
        "labs": evaluate_labs(labs_dir),
        "slides": evaluate_slides(module_dir),
    }


def main():
    dashboard = json.loads(DASHBOARD_PATH.read_text(encoding="utf-8"))
    for m in dashboard["modules"]:
        result = evaluate_module(m, REPO_ROOT)
        m["name"] = result["name"]
        m["path"] = result["path"]
        m["theory"] = result["theory"]
        m["demos"] = result["demos"]
        m["labs"] = result["labs"]
        m["slides"] = result["slides"]
    DASHBOARD_PATH.write_text(json.dumps(dashboard, indent=2), encoding="utf-8")
    print(f"Evaluated {len(dashboard['modules'])} modules -> {DASHBOARD_PATH}")


if __name__ == "__main__":
    main()
