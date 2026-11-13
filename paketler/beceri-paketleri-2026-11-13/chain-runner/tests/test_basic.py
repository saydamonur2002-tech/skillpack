# Minimal test: chain with single known pack
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "main.py"

PACKS = ROOT.parent  # sibling pack directories live next to chain-runner


def test_single_idna():
    payload = {
        "user_input": "münchen",
        "steps": [{"pack": "idna-encode", "from": "user"}]
    }
    p = subprocess.run(
        [sys.executable, str(MAIN)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env={**__import__("os").environ, "SKILLPACK_PACKS_DIR": str(PACKS)},
    )
    assert p.returncode == 0, p.stdout + p.stderr
    data = json.loads(p.stdout)
    assert data["result"] == "xn--mnchen-3ya"

if __name__ == "__main__":
    test_single_idna()
    print("chain-runner tests passed")
