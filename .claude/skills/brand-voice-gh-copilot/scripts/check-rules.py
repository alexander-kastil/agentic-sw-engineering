"""Check the mechanical rules in references/rules.md.

usage: python check-rules.py <path> [<path> ...]

A path may be a file or a directory; directories are searched for readme.md,
skipping pptx/. Reports one line per violation and an assertable summary.
Exit 1 when any violation is found.

Covers rules 1, 2, 4, 5, 6, 7, 10 and 11. Rules 3, 8 and 9 need judgement and
are left to the skill.
"""

import os
import re
import sys

MAX_SENTENCES = 4
MAX_NOTES = 3
MAX_NODES = 6
MAX_LINKS = 4
MIN_LINKS = 1
MAX_DIAGRAMS = 3
MIN_DIAGRAMS = 1

SKIP_PREFIXES = ("#", ">", "|", "-", "*", "[", "!")
HTML_TABLE = re.compile(r"</?(table|thead|tbody|tr|td|th|col|colgroup)\b", re.I)
NODE = re.compile(r"(?:^|\s)([A-Za-z][A-Za-z0-9_]*)\s*(\[|\{|\()")
UNQUOTED = re.compile(r"[\[\{(]{1,2}(?![\"'])[^\"\]\})]*[a-z][^\"\]\})]*[\]\})]{1,2}")


def targets(paths):
    out = []
    for p in paths:
        if os.path.isfile(p):
            out.append(p)
            continue
        for root, dirs, names in os.walk(p):
            dirs[:] = [d for d in dirs if d not in ("pptx", ".git", "node_modules")]
            if "readme.md" in names:
                out.append(os.path.join(root, "readme.md"))
    return sorted(set(out))


def check(path):
    bad = []
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    in_mermaid = False
    in_fence = False
    in_links = False
    links = 0
    notes = 0
    diagrams = 0
    nodes = set()
    start = 0
    after_links = 0

    for i, line in enumerate(lines, 1):
        if line.startswith("```mermaid"):
            in_mermaid, in_fence, diagrams, nodes, start = True, True, diagrams + 1, set(), i
            continue
        if line.startswith("```"):
            if in_mermaid and len(nodes) > MAX_NODES:
                bad.append(f"{path}:{start} [rule7] diagram has {len(nodes)} nodes, max {MAX_NODES}")
            in_mermaid = False
            in_fence = not in_fence if not in_mermaid else False
            continue
        if in_mermaid:
            nodes |= {m.group(1) for m in NODE.finditer(line)}
            if "\\n" in line:
                bad.append(f"{path}:{i} [rule5] literal \\n in a mermaid label, use <br/>")
            body = re.sub(r"-->\|[^|]*\|", "", line)
            if UNQUOTED.search(body):
                bad.append(f"{path}:{i} [rule5] unquoted mermaid node label")
            continue
        if in_fence:
            continue

        if "—" in line or "–" in line or "&mdash;" in line:
            bad.append(f"{path}:{i} [rule1] em dash in prose")
        if HTML_TABLE.search(line):
            bad.append(f"{path}:{i} [rule11] HTML table element")
        if line.startswith("> Note:"):
            notes += 1
        if line.startswith("## Links & Resources"):
            in_links = True
            continue
        if in_links:
            if line.startswith("- ["):
                links += 1
            elif line.startswith("#"):
                after_links += 1
        if line.startswith(SKIP_PREFIXES) or not line.strip() or re.match(r"^\d+\.", line):
            continue
        n = len(re.findall(r"[.!?](?:\s|$)", line))
        if n > MAX_SENTENCES:
            bad.append(f"{path}:{i} [rule2] paragraph has {n} sentences, max {MAX_SENTENCES}")

    if notes > MAX_NOTES:
        bad.append(f"{path} [rule4] {notes} Note callouts, max {MAX_NOTES}")
    if not in_links:
        bad.append(f"{path} [rule10] no Links & Resources section")
    else:
        if not MIN_LINKS <= links <= MAX_LINKS:
            bad.append(f"{path} [rule10] {links} links, allowed {MIN_LINKS} to {MAX_LINKS}")
        if after_links:
            bad.append(f"{path} [rule10] {after_links} heading(s) after Links & Resources")
    topic = os.path.dirname(os.path.abspath(path))
    if os.path.basename(topic)[:2].isdigit() and os.path.basename(os.path.dirname(topic))[:2].isdigit():
        if not MIN_DIAGRAMS <= diagrams <= MAX_DIAGRAMS:
            bad.append(f"{path} [rule6] {diagrams} mermaid diagrams, allowed {MIN_DIAGRAMS} to {MAX_DIAGRAMS}")
    return bad


def main():
    paths = sys.argv[1:] or ["."]
    files = targets(paths)
    found = []
    for f in files:
        found.extend(check(f))
    for line in found:
        print(line)
    print(f"files={len(files)} violations={len(found)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
