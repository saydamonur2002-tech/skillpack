#!/usr/bin/env python3
"""Scaffold a new skill pack skeleton."""
import argparse
import json
import os
from pathlib import Path

TEMPLATE_SKILL = """---
name: {name}
description: "TODO: single function description. Use when X."
---

# {name}

Thin wrapper around a single library function.

## Input
`{{"input": ...}}`

## Output
`{{"result": ...}}`

## Limits
- Offline only
- Requires installed library: {source}
"""

TEMPLATE_MANIFEST = {
    "name": "{name}",
    "source": "{source}",
    "function": "{function}",
    "truth_level": "sozlesme",
    "license": "TODO: SPDX + full text path",
    "version": "0.1.0"
}

TEMPLATE_MAIN = '''#!/usr/bin/env python3
import json
import sys

# TODO: import the real library
# import idna

def main():
    raw = sys.stdin.read()
    data = json.loads(raw)
    inp = data.get("input")
    
    # TODO: call the single function
    # result = idna.encode(inp).decode()
    result = {"echo": inp}  # placeholder
    
    print(json.dumps({"result": result}))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--source", default="TODO-package==1.0")
    parser.add_argument("--function", default="TODO.function")
    parser.add_argument("--out", default="/workspace/skillpacks")
    args = parser.parse_args()

    root = Path(args.out) / args.name
    root.mkdir(parents=True, exist_ok=True)
    (root / "scripts").mkdir(exist_ok=True)
    (root / "tests").mkdir(exist_ok=True)
    (root / "references").mkdir(exist_ok=True)
    (root / "schema").mkdir(exist_ok=True)

    (root / "SKILL.md").write_text(TEMPLATE_SKILL.format(name=args.name, source=args.source))
    manifest = {
        "name": args.name,
        "source": args.source,
        "function": args.function,
        "truth_level": "sozlesme",
        "license": "TODO: SPDX + full text path",
        "version": "0.1.0"
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (root / "scripts" / "main.py").write_text(TEMPLATE_MAIN)
    (root / "scripts" / "main.py").chmod(0o755)
    (root / "tests" / "test_basic.py").write_text("# TODO: add tests with documented vector origins\\n")
    (root / "references" / "LICENSE.txt").write_text("TODO: paste full license text\\n")

    print(f"Scaffolded {root}")

if __name__ == "__main__":
    main()
