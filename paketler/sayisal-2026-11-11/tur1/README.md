# Ten tested mined skillpacks — 2026-11-11

Use **mined-packs-2026-11-11.tar.gz**, not the old RESEARCH-ONLY archive. That earlier file is superseded historical research, not an installable pack release.

This release contains M001–M010. All 261 tests passed. Read MINING_REPORT.md for provenance, exact scope and limitations, and LICENSE_INDEX.md for the original notices.

## Verify and unpack

```sh
sha256sum -c SHA256SUMS
tar -xzf mined-packs-2026-11-11.tar.gz
cd mined_packs_2026-11-11
```

The archive is under 8 MB; it is not split. Each Mxxx directory is independently usable and includes FILES.sha256.

## Install and test the batch

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m pytest -q
.venv/bin/python M003/tool/main.py < M003/example.json
```

Python 3.11+ on Linux is required; the CLI watchdog uses POSIX alarms. Dependencies are not bundled. Calculation code uses the standard library; schema validation and MCP require the pinned packages.

For a single pack, enter its directory, install its requirements, and run `python tool/main.py < example.json` or `pytest tests`. Each pack's SKILL.md gives a stdio MCP configuration; replace absolute path placeholders with actual local paths. No server account or hosted backend is needed.

`upstream/` contains license/source/test evidence, not code to execute; pytest is configured not to collect it. The model explains a deterministic result, and a human reviews consequential use.
