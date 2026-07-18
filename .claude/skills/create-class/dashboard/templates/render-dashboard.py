#!/usr/bin/env python3
"""Render the local class progress dashboard.

Reads:
  - dashboard/dashboard.json  (module config + evaluated status fields)

Writes:
  - dashboard/index.html  (data injected inline between DATA markers)
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_contributors import collect as collect_contributors, build_pr_contributor_map, get_path_contributors, get_lab_contributors

MODULE_PREFIX_RE = re.compile(
    r"^(?:Module\s+\d+(?:\.\d+)*|\d+)\s*[:\-–—]\s*",
    re.IGNORECASE,
)


def strip_module_prefix(title):
    return MODULE_PREFIX_RE.sub("", title).strip()


LAB_FILE_RE = re.compile(r"^lab-\d+.*\.md$", re.IGNORECASE)
DEMO_FILE_RE = re.compile(r"^(?:\d{2}-demo-|demo-\d{2}-).*\.md$", re.IGNORECASE)


def read_h1(file_path):
    if not file_path.exists():
        return ""
    for line in file_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def list_labs(module_path, pr_map):
    if not module_path:
        return []
    module_dir_name = module_path.split("/")[-1]
    labs_dir = REPO_ROOT / "labs" / module_dir_name
    if not labs_dir.exists():
        return []

    sub_dir_labs = []
    for child in sorted(labs_dir.iterdir()):
        if not child.is_dir() or not child.name[:2].isdigit():
            continue
        readme = child / "readme.md"
        if not readme.exists():
            readme = child / "README.md"
        if not readme.exists():
            continue
        title = read_h1(readme)
        if not title:
            continue
        lab_num = len(sub_dir_labs) + 1
        lab_rel = f"labs/{module_dir_name}/{child.name}"
        sub_dir_labs.append({
            "number": lab_num,
            "slug": child.name,
            "title": title,
            "path": lab_rel,
            "contributors": get_lab_contributors(f"labs/{module_dir_name}", lab_num, pr_map),
        })
    if sub_dir_labs:
        return sub_dir_labs

    flat_labs = []
    for f in sorted(labs_dir.iterdir()):
        if not f.is_file() or not LAB_FILE_RE.match(f.name):
            continue
        title = read_h1(f)
        if not title:
            continue
        flat_rel = f"labs/{module_dir_name}/{f.name}"
        lab_num = len(flat_labs) + 1
        flat_labs.append({
            "number": lab_num,
            "slug": f.stem,
            "title": title,
            "path": flat_rel,
            "contributors": get_lab_contributors(f"labs/{module_dir_name}", lab_num, pr_map),
        })
    return flat_labs


def list_module_demos(module_dir, module_path, pr_map):
    if not module_dir or not module_dir.exists():
        return []
    demos_sub = module_dir / "demos"
    if demos_sub.is_dir():
        base_dir, base_rel = demos_sub, f"{module_path}/demos"
    else:
        base_dir, base_rel = module_dir, module_path
    demos = []
    for f in sorted(base_dir.iterdir()):
        if not f.is_file() or not DEMO_FILE_RE.match(f.name):
            continue
        title = read_h1(f)
        if not title:
            continue
        demo_rel = f"{base_rel}/{f.name}"
        demos.append({
            "number": len(demos) + 1,
            "slug": f.stem,
            "title": title,
            "path": demo_rel,
            "contributors": get_path_contributors(demo_rel, pr_map),
        })
    return demos

DASHBOARD_DIR = Path(__file__).resolve().parent
REPO_ROOT = DASHBOARD_DIR.parent
DASHBOARD_PATH = DASHBOARD_DIR / "dashboard.json"
README_PATH = REPO_ROOT / "README.md"
INDEX_PATH = DASHBOARD_DIR / "index.html"
DATA_START = "<!-- DATA:START -->"
DATA_END = "<!-- DATA:END -->"

START_MARKER = "<!-- DASHBOARD:START -->"
END_MARKER = "<!-- DASHBOARD:END -->"

COMPONENT_KEYS = ("theory", "demos", "labs", "slides")

STATUS_EMOJI = {"done": "🟢", "almost": "🔵", "doing": "🟡", "planned": "🔴"}
STEP_EMOJI = ["🟥", "🟨", "🟦", "🟩"]
EMPTY_EMOJI = "⬜"
SUB_STATUS_EMOJI = {"done": "🟢", "doing": "🟡", "planned": "⚪"}


def module_status(done_count, total):
    if total == 0:
        return "planned"
    if done_count == total:
        return "done"
    if done_count == 0:
        return "planned"
    if done_count / total >= 0.75:
        return "almost"
    return "doing"


def progress_bar(done_count, total=4):
    return "▰" * done_count + "▱" * (total - done_count)


def read_full_name(path):
    if not path:
        return ""
    readme = REPO_ROOT / path / "readme.md"
    if not readme.exists():
        return ""
    for line in readme.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return strip_module_prefix(stripped[2:].strip())
    return ""


def list_topics(path, pr_map):
    if not path:
        return []
    module_dir = REPO_ROOT / path
    if not module_dir.exists():
        return []
    topics = []
    counter = 0
    for child in sorted(module_dir.iterdir()):
        if not child.is_dir():
            continue
        if not child.name[:2].isdigit():
            continue
        readme = child / "readme.md"
        if not readme.exists():
            continue
        title = ""
        for line in readme.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                title = strip_module_prefix(stripped[2:].strip())
                break
        if not title:
            continue
        counter += 1
        topic_rel = f"{path}/{child.name}"
        topics.append({
            "number": counter,
            "slug": child.name,
            "title": title,
            "path": topic_rel,
            "contributors": get_path_contributors(topic_rel, pr_map),
        })
    return topics


def build_payload(dashboard):
    pr_map = build_pr_contributor_map()
    modules_in = list(dashboard["modules"])
    modules_in.sort(key=lambda m: m["num"])

    out_modules = []
    total_subs = 0
    total_done = 0
    for m in modules_in:
        sub_out = []
        for sub in m["subItems"]:
            key = sub["key"]
            status = m.get(key, "planned")
            entry = {
                "key": key,
                "label": sub["label"],
                "status": status,
            }
            if "issueNumber" in sub:
                entry["issueNumber"] = sub["issueNumber"]
            sub_out.append(entry)
            if status != "absent":
                total_subs += 1
                if status == "done":
                    total_done += 1

        applicable = [s["status"] for s in sub_out if s["status"] != "absent"]
        total_count = len(applicable)
        done_count = sum(1 for s in applicable if s == "done")
        mod = {
            "num": m["num"],
            "name": m["name"],
            "assignee": m.get("assignee", ""),
            "status": module_status(done_count, total_count),
            "progress": {
                "done": done_count,
                "total": total_count,
                "percent": int(round(done_count / total_count * 100)) if total_count else 0,
            },
            "subItems": sub_out,
        }
        if "issueNumber" in m:
            mod["issueNumber"] = m["issueNumber"]
        if "path" in m:
            mod["path"] = m["path"]
        full = read_full_name(m.get("path", ""))
        if full:
            mod["fullName"] = full
        topics = list_topics(m.get("path", ""), pr_map)
        if topics:
            mod["topics"] = topics
        module_path = m.get("path", "")
        module_dir = REPO_ROOT / module_path if module_path else None
        demos = list_module_demos(module_dir, module_path, pr_map)
        for md in m.get("manualDemos", []):
            if not any(d["path"] == md["path"] for d in demos):
                demos.append({
                    "number": len(demos) + 1,
                    "slug": Path(md["path"]).stem,
                    "title": md["title"],
                    "path": md["path"],
                    "contributors": get_path_contributors(md["path"], pr_map),
                })
        if demos:
            mod["demos"] = demos
        labs = list_labs(m.get("path", ""), pr_map)
        if labs:
            mod["labs"] = labs
        out_modules.append(mod)

    overall_pct = int(round(total_done / total_subs * 100)) if total_subs else 0
    return {
        "project": dashboard["project"],
        "modules": out_modules,
        "summary": {
            "totalModules": len(out_modules),
            "totalSubs": total_subs,
            "done": total_done,
            "percent": overall_pct,
        },
        "contributors": collect_contributors(),
    }


def write_app_data(payload):
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    script_block = f"<script>window.DASHBOARD_DATA = {body};</script>"
    new_block = f"{DATA_START}\n{script_block}\n{DATA_END}"
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    pre, rest = index_text.split(DATA_START, 1)
    _, post = rest.split(DATA_END, 1)
    INDEX_PATH.write_text(f"{pre}{new_block}{post}", encoding="utf-8")


def gradient_bar(done, total=4):
    return "".join(STEP_EMOJI[i] if i < done else EMPTY_EMOJI for i in range(total))


def avatar_html(user):
    if not user:
        return "_unassigned_"
    return (
        f'<img src="https://github.com/{user}.png?size=40" width="20" height="20" '
        f'align="absmiddle" alt="" /> @{user}'
    )


def issue_url(repo, number):
    return f"https://github.com/{repo}/issues/{number}"


def render_readme_block(payload):
    project = payload["project"]
    repo = project["repo"]
    s = payload["summary"]

    live_url = project.get("pagesUrl") or f"https://raw.githack.com/{repo}/master/dashboard/index.html"

    lines = [
        f'[![Open Live Dashboard](https://img.shields.io/badge/%F0%9F%93%8A%20Open%20Live%20Dashboard-2da44e?style=for-the-badge&logoColor=white)]({live_url})',
        "",
        f'> 🔗 **[{live_url}]({live_url})** &nbsp;·&nbsp; '
        f'**[GitHub project board]({project["projectUrl"]})** &nbsp;·&nbsp; '
        f'source: `dashboard/index.html`',
        "",
        f"**{s['totalModules']} modules** · {s['done']}/{s['totalSubs']} sub-items done · **{s['percent']}%** complete &nbsp; "
        f"🔴 planned &nbsp; 🟡 doing &nbsp; 🔵 almost &nbsp; 🟢 done",
        "",
        "| # | Module | Assignee | Progress | Status |",
        "|---|---|---|---|---|",
    ]

    for i, m in enumerate(payload["modules"], start=1):
        prog = m["progress"]
        bar = gradient_bar(prog["done"], prog["total"])
        title_text = f"Module {m['num']} - {m['name']}"
        if m.get("issueNumber"):
            title_html = f'<a href="{issue_url(repo, m["issueNumber"])}"><b>{title_text}</b></a> <a href="{issue_url(repo, m["issueNumber"])}">#{m["issueNumber"]}</a>'
        else:
            title_html = f"<b>{title_text}</b>"
        emoji = STATUS_EMOJI[m["status"]]
        lines.append(
            f"| {i} "
            f"| {emoji} {title_html} "
            f"| {avatar_html(m['assignee'])} "
            f"| {bar} &nbsp; {prog['done']}/{prog['total']} &nbsp; {prog['percent']}% "
            f"| {emoji} **{m['status']}** |"
        )

    lines.append("")
    lines.append("<details>")
    lines.append("<summary><b>Sub-issue breakdown</b> (click to expand)</summary>")
    lines.append("")
    lines.append("| Module | Theory | Code Demos | Labs | Slides |")
    lines.append("|---|---|---|---|---|")
    for m in payload["modules"]:
        cells = [f"**Module {m['num']} - {m['name']}**"]
        sub_by_key = {s["key"]: s for s in m["subItems"]}
        for key in ("theory", "demos", "labs", "slides"):
            sub = sub_by_key.get(key)
            if not sub:
                cells.append("—")
                continue
            icon = SUB_STATUS_EMOJI[sub["status"]]
            if sub.get("issueNumber"):
                cells.append(f'{icon} [{sub["status"]}]({issue_url(repo, sub["issueNumber"])})')
            else:
                cells.append(f"{icon} {sub['status']}")
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("</details>")

    return "\n".join(lines)


def splice_readme(readme_text, content):
    block = f"{START_MARKER}\n{content}\n{END_MARKER}"
    if START_MARKER in readme_text and END_MARKER in readme_text:
        pre, rest = readme_text.split(START_MARKER, 1)
        _, post = rest.split(END_MARKER, 1)
        return f"{pre}{block}{post}"
    suffix = "" if readme_text.endswith("\n") else "\n"
    return f"{readme_text}{suffix}\n## Class Progress\n\n{block}\n"


def main():
    dashboard = json.loads(DASHBOARD_PATH.read_text(encoding="utf-8"))
    payload = build_payload(dashboard)

    write_app_data(payload)


if __name__ == "__main__":
    main()
