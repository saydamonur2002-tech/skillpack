# Basic operator tests
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main.py"

def call(payload):
    p = subprocess.run(
        [sys.executable, str(MAIN)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
    )
    return p.returncode, p.stdout, p.stderr

def test_help():
    code, out, err = call({"command": "help"})
    assert code == 0
    data = json.loads(out)
    assert "help" in data["result"]["stdout"]

if __name__ == "__main__":
    test_help()
    print("operator tests passed")
