import os, re, sys

HISTORICAL = re.compile(r"^(\.claude/verification/|\.time/|tasks/lessons\.md|tasks/open-issues\.md|HISTORY\.md)")
SKIP_DIRS = {".git", "node_modules", "dist", "bin", "obj", ".venv", "site-packages", "out", ".angular", "__pycache__"}
TEXT_EXT = {".md", ".txt", ".json", ".yaml", ".yml", ".sh", ".ps1", ".py", ".js", ".ts", ".html", ".css",
            ".example", ".env", ".tsv", ".toml", ".slnx", ".csproj", ".cs", ".conf", ".xml", ""}

def scan(root, targets):
    pats = {t: re.compile(r"(?<![A-Za-z0-9._\-])" + re.escape(os.path.basename(t))) for t in targets}
    found = {t: {"live": [], "hist": 0} for t in targets}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT and not fn.startswith(".env"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            try:
                with open(full, encoding="utf-8", errors="ignore") as fh:
                    lines = fh.readlines()
            except OSError:
                continue
            for t, pat in pats.items():
                if rel == t:
                    continue
                for i, line in enumerate(lines, 1):
                    if pat.search(line):
                        if HISTORICAL.match(rel):
                            found[t]["hist"] += 1
                        else:
                            found[t]["live"].append(f"{rel}:{i}:{line.strip()[:160]}")
    return found

def main():
    if len(sys.argv) < 3:
        print("usage: doc-refs.py <repo-root> <doc-path> [...]", file=sys.stderr)
        return 2
    root, targets = sys.argv[1], sys.argv[2:]
    res = scan(root, targets)
    stale = 0
    for t in targets:
        print(f"=== {t} ===")
        for hit in res[t]["live"]:
            print(f"  LIVE {hit}")
        if os.path.exists(os.path.join(root, t)):
            print("  NOTE the path still exists, so every LIVE hit is ambiguous between the old")
            print("       and the new occupant. Open each one and decide which content it means.")
        elif res[t]["live"]:
            stale += len(res[t]["live"])
        print(f"  live={len(res[t]['live'])} historical={res[t]['hist']}"
              "  (historical are records; never retarget them)")
    print(f"\nstale references to non-existent paths: {stale}")
    return 1 if stale else 0

sys.exit(main())
