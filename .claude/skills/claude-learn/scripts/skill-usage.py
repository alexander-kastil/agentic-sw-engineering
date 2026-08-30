#!/usr/bin/env python3
"""Registry of installed skills against their real invocation history.

Reads every Claude Code session transcript under ~/.claude/projects/*/*.jsonl,
counts Skill tool calls per skill name, and joins that against the skills
installed globally (~/.claude/skills) and locally (<repo>/.claude/skills).

Usage: python skill-usage.py [repo-root] [--days N] [--json]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HOME = Path.home()
PROJECTS = HOME / ".claude" / "projects"
GLOBAL_SKILLS = HOME / ".claude" / "skills"

def installed(root):
    """name -> mtime of its SKILL.md, a weak hint at how long it has existed."""
    if not root.is_dir():
        return {}
    out = {}
    for d in root.iterdir():
        manifest = d / "SKILL.md"
        if manifest.is_file():
            out[d.name] = manifest.stat().st_mtime
    return out

def invocations():
    """name -> (last_iso, count). Substring prefilter keeps the scan cheap."""
    seen = {}
    for path in PROJECTS.glob("*/*.jsonl"):
        try:
            fh = path.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                if '"Skill"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                content = (rec.get("message") or {}).get("content") or []
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") != "tool_use" or block.get("name") != "Skill":
                        continue
                    name = (block.get("input") or {}).get("skill")
                    if not name:
                        continue
                    name = name.split(":")[-1]
                    stamp = rec.get("timestamp") or ""
                    last, count = seen.get(name, ("", 0))
                    seen[name] = (max(last, stamp), count + 1)
    return seen

def age_days(stamp, now):
    if not stamp:
        return None
    try:
        when = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (now - when).days

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    local_root = Path(args.repo).resolve() / ".claude" / "skills"
    scopes, written = {}, {}
    for name, mtime in installed(GLOBAL_SKILLS).items():
        scopes[name] = "global"
        written[name] = mtime
    for name, mtime in installed(local_root).items():
        scopes[name] = "both" if name in scopes else "local"
        written[name] = max(written.get(name, 0), mtime)

    used = invocations()
    now = datetime.now(timezone.utc)

    rows = []
    for name in sorted(scopes):
        last, count = used.get(name, ("", 0))
        days = age_days(last, now)
        fresh = (now.timestamp() - written[name]) / 86400 < args.days
        if count == 0:
            status = "NEW" if fresh else "NEVER"
        elif days is not None and days > args.days:
            status = "STALE"
        else:
            status = "ACTIVE"
        rows.append(
            {
                "skill": name,
                "scope": scopes[name],
                "last_used": last[:10] if last else "-",
                "days_ago": days if days is not None else "-",
                "invocations": count,
                "status": status,
            }
        )

    orphans = sorted(set(used) - set(scopes))

    if args.json:
        print(json.dumps({"rows": rows, "orphans": orphans}, indent=2))
        return

    order = {"NEVER": 0, "STALE": 1, "NEW": 2, "ACTIVE": 3}
    rows.sort(key=lambda r: (order[r["status"]], -r["invocations"], r["skill"]))
    width = max([len(r["skill"]) for r in rows] + [5])
    print(f"{'skill'.ljust(width)}  scope   last used   uses  status")
    for r in rows:
        print(
            f"{r['skill'].ljust(width)}  {r['scope']:<6}  {r['last_used']:<10}  "
            f"{r['invocations']:>4}  {r['status']}"
        )
    if orphans:
        print("\nInvoked but not installed (renamed or removed): " + ", ".join(orphans))

if __name__ == "__main__":
    main()
