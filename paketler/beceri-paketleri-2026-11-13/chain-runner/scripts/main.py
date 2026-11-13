#!/usr/bin/env python3
"""Chain runner: execute a sequence of skillpacks.
Input: {"steps": [{"pack": "name", "input": ... or "from": "previous"|"user"}, ...], "user_input": ...}
"""
import json
import os
import sys
import subprocess
import tempfile
import zipfile
from pathlib import Path

PACKS_DIR = Path(os.environ.get("SKILLPACK_PACKS_DIR", "/workspace/skillpacks"))

def load_pack(name: str) -> Path:
    """Return path to unpacked pack directory. Supports .zip or directory."""
    zip_path = PACKS_DIR / f"{name}.zip"
    dir_path = PACKS_DIR / name
    if dir_path.is_dir() and (dir_path / "scripts" / "main.py").exists():
        return dir_path
    if zip_path.exists():
        extract_to = Path(tempfile.mkdtemp(prefix=f"pack-{name}-"))
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_to)
        return extract_to
    raise FileNotFoundError(f"Pack not found: {name}")

def call_pack(pack_dir: Path, inp):
    main = pack_dir / "scripts" / "main.py"
    if not main.exists():
        raise FileNotFoundError(f"No main.py in {pack_dir}")
    p = subprocess.run(
        [sys.executable, str(main)],
        input=json.dumps({"input": inp}),
        text=True,
        capture_output=True,
    )
    if p.returncode != 0:
        try:
            err = json.loads(p.stdout)
        except Exception:
            err = {"error": p.stdout or p.stderr}
        raise RuntimeError(err)
    return json.loads(p.stdout)["result"]

def main():
    raw = sys.stdin.read()
    data = json.loads(raw)
    steps = data.get("steps", [])
    user_input = data.get("user_input")
    previous = None
    trace = []

    for i, step in enumerate(steps):
        pack_name = step["pack"]
        if "input" in step:
            current_input = step["input"]
        elif step.get("from") == "user":
            current_input = user_input
        elif step.get("from") == "previous" or previous is not None:
            current_input = previous
        else:
            current_input = user_input

        pack_dir = load_pack(pack_name)
        result = call_pack(pack_dir, current_input)
        trace.append({"step": i, "pack": pack_name, "input": current_input, "output": result})
        previous = result

    print(json.dumps({"result": previous, "trace": trace}))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}))
        sys.exit(1)
