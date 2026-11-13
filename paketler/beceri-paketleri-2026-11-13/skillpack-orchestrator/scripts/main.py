#!/usr/bin/env python3
"""Operator entry point for skillpack-orchestrator.
Accepts commands via stdin JSON to scaffold, validate, or zip packs.
"""
import json
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

def run_script(script_name, args):
    cmd = [sys.executable, str(SCRIPTS / script_name)] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "returncode": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr
    }

def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    cmd = data.get("command")
    args = data.get("args", [])

    if cmd == "scaffold":
        result = run_script("scaffold_pack.py", args)
    elif cmd == "validate":
        result = run_script("validate_pack.py", args)
    elif cmd == "zip":
        result = run_script("make_deterministic_zip.py", args)
    elif cmd == "help":
        result = {
            "returncode": 0,
            "stdout": "commands: scaffold, validate, zip, help",
            "stderr": ""
        }
    else:
        print(json.dumps({"error": "unknown command", "available": ["scaffold", "validate", "zip", "help"]}))
        sys.exit(1)

    print(json.dumps({"result": result}))
    if result.get("returncode", 0) != 0:
        sys.exit(result["returncode"])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}))
        sys.exit(1)
