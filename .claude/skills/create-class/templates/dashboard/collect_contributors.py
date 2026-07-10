#!/usr/bin/env python3
"""Collect git contributor stats: commits, lines added, and contribution percentage."""

import subprocess
import json
from pathlib import Path
from collections import defaultdict

GITHUB_LOGINS = {
    "alexander.kastil@integrations.at": "alexander-kastil",
    "chrisveres1@gmail.com": "Tikket",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = Path(__file__).resolve().parent
OVERRIDES_PATH = DASHBOARD_DIR / "contributors-override.json"


def _load_overrides():
    if not OVERRIDES_PATH.exists():
        return {}
    return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))


def collect():
    result = subprocess.run(
        ["git", "log", "--format=COMMIT|%an|%ae", "--shortstat"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )

    authors = defaultdict(lambda: {"name": "", "email": "", "commits": 0, "lines": 0})
    current_email = None

    for line in result.stdout.splitlines():
        if line.startswith("COMMIT|"):
            _, name, email = line.split("|", 2)
            email = email.strip()
            current_email = email
            authors[email]["name"] = name.strip()
            authors[email]["email"] = email
            authors[email]["commits"] += 1
        elif current_email and ("insertion" in line or "deletion" in line):
            for part in line.split(","):
                part = part.strip()
                if "insertion" in part:
                    try:
                        authors[current_email]["lines"] += int(part.split()[0])
                    except (ValueError, IndexError):
                        pass

    total_lines = sum(a["lines"] for a in authors.values()) or 1

    contributors = []
    for email, a in sorted(authors.items(), key=lambda kv: -kv[1]["lines"]):
        pct = round(a["lines"] / total_lines * 100)
        contributors.append({
            "name": a["name"],
            "github": GITHUB_LOGINS.get(email, ""),
            "commits": a["commits"],
            "linesAdded": a["lines"],
            "percent": pct,
        })

    diff = 100 - sum(c["percent"] for c in contributors)
    if contributors and diff != 0:
        contributors[0]["percent"] += diff

    return contributors


def build_pr_contributor_map():
    """Fetch all merged PRs from GitHub and return {file_path: [login, ...]}."""
    result = subprocess.run(
        ["gh", "pr", "list", "--state", "merged", "--json", "author,files", "--limit", "200"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return {}
    prs = json.loads(result.stdout)
    path_map = {}
    for pr in prs:
        login = pr["author"]["login"]
        for f in pr.get("files", []):
            p = f["path"]
            if p not in path_map:
                path_map[p] = []
            if login not in path_map[p]:
                path_map[p].append(login)
    return path_map


def _git_path_authors(rel_path):
    """Return GitHub logins from git history for a repo-relative path."""
    result = subprocess.run(
        ["git", "log", "--format=%ae", "--", rel_path],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    seen = {}
    for email in result.stdout.splitlines():
        handle = GITHUB_LOGINS.get(email.strip())
        if handle and handle not in seen:
            seen[handle] = True
    return list(seen.keys())


def get_path_contributors(rel_path, pr_map):
    """Return ordered list of GitHub logins for contributors to a repo-relative path.

    Prefers merged-PR authorship; falls back to git history when no PR touched the path.
    """
    seen = {}
    prefix = rel_path.rstrip("/") + "/"
    for file_path, authors in pr_map.items():
        if file_path == rel_path or file_path.startswith(prefix):
            for login in authors:
                if login not in seen:
                    seen[login] = True
    if not seen:
        for login in _git_path_authors(rel_path):
            seen[login] = True
    return list(seen.keys())


def get_lab_contributors(module_labs_prefix, lab_number, pr_map):
    """Return contributors for a lab using PR data, with override file as correction layer."""
    num = f"{int(lab_number):02d}-"
    prefix = module_labs_prefix.rstrip("/") + "/"
    seen = {}
    for file_path, authors in pr_map.items():
        if not file_path.startswith(prefix):
            continue
        remainder = file_path[len(prefix):]
        if remainder.startswith(num) or remainder.startswith(f"lab-{num}"):
            for login in authors:
                if login not in seen:
                    seen[login] = True
    if not seen:
        result = subprocess.run(
            ["git", "log", "--format=%ae", "--", module_labs_prefix],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        for email in result.stdout.splitlines():
            handle = GITHUB_LOGINS.get(email.strip())
            if handle and handle not in seen:
                seen[handle] = True
    overrides = _load_overrides()
    for login in overrides.get("labs", {}).get(module_labs_prefix, {}).get(str(lab_number), []):
        if login not in seen:
            seen[login] = True
    return list(seen.keys())


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
