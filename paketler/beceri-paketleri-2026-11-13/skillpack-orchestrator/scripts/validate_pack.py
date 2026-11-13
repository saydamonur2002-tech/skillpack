#!/usr/bin/env python3
"""Basic local validation for a skill pack. Maps to subset of C01-C11."""
import json
import subprocess
import sys
from pathlib import Path

def check(path: Path):
    results = []
    def add(control, status, detail=""):
        results.append({"control": control, "status": status, "detail": detail})

    if not (path / "SKILL.md").exists():
        add("C01", "FAIL", "missing SKILL.md")
    else:
        text = (path / "SKILL.md").read_text()
        if "---" in text and "name:" in text:
            add("C01", "PASS", "YAML frontmatter present")
        else:
            add("C01", "FAIL", "no YAML frontmatter")

    if not (path / "manifest.json").exists():
        add("structure", "FAIL", "missing manifest.json")
    else:
        try:
            m = json.loads((path / "manifest.json").read_text())
            add("structure", "PASS", f"manifest ok, truth_level={m.get('truth_level')}")
        except Exception as e:
            add("structure", "FAIL", str(e))

    main = path / "scripts" / "main.py"
    if not main.exists():
        add("C09", "FAIL", "missing scripts/main.py")
    else:
        code = main.read_text()
        if any(x in code for x in ["requests.", "urllib.request", "http.client", "socket."]):
            add("C09", "FAIL", "possible network import")
        else:
            add("C09", "PASS", "no obvious network imports")

    if not (path / "tests").exists() or not list((path / "tests").iterdir()):
        add("C04", "FAIL", "no tests")
    else:
        add("C04", "PASS", "tests directory present (run them separately)")

    lic = path / "references" / "LICENSE.txt"
    if lic.exists() and lic.stat().st_size > 20:
        add("C03", "PASS", "license text present")
    else:
        add("C03", "FAIL", "missing or empty license")

    print(json.dumps({"pack": str(path), "results": results}, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate_pack.py <pack-dir>")
        sys.exit(1)
    check(Path(sys.argv[1]))
