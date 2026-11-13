# Simple functional tests for idna-encode
# Vector origins: well-known IDNA examples (münchen, bücher)

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main.py"

def call(inp):
    p = subprocess.run(
        [sys.executable, str(MAIN)],
        input=json.dumps({"input": inp}),
        text=True,
        capture_output=True,
    )
    if p.returncode != 0:
        raise RuntimeError(p.stdout + p.stderr)
    return json.loads(p.stdout)["result"]

def test_muenchen():
    assert call("münchen") == "xn--mnchen-3ya"

def test_buecher():
    assert call("bücher") == "xn--bcher-kva"

if __name__ == "__main__":
    test_muenchen()
    test_buecher()
    print("tests passed")
