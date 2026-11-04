"""Validate this plugin's manifests against the schemas they declare."""
import json
import sys
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def validate(name: str) -> int:
    path = ROOT / name
    if not path.exists():
        print(f"{name}: MISSING")
        return 1

    document = json.loads(path.read_text(encoding="utf-8"))
    schema_url = document.get("$schema")
    if not schema_url:
        print(f"{name}: INVALID")
        print("   '$schema' is a required property")
        return 1

    schema = json.load(urllib.request.urlopen(schema_url))
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: str(e.path))
    if not errors:
        print(f"{name}: VALID")
        return 0

    print(f"{name}: INVALID")
    for error in errors:
        location = "/".join(str(p) for p in error.path) or "(root)"
        print(f"   {location}: {error.message}")
    return 1


if __name__ == "__main__":
    sys.exit(max(validate("plugin.json"), validate("mcp.json")))
