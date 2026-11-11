# Mined numerical skillpacks — Round 2

Ten new standalone packs, M011–M020. Start with MINING_REPORT.md, LICENSE_INDEX.md and each pack SKILL.md / TEACHING.md. Numerical source evidence is pinned, not downloaded at runtime. No existing repo was changed.

## Verify and extract

```sh
sha256sum -c SHA256SUMS
tar -xzf mined-packs-2026-11-11b.tar.gz
cd mined_packs_2026-11-11b
python3 -m venv .venv
.venv/bin/python -m pip install -r M011/requirements-test.txt
.venv/bin/python -m pytest -q
```

The full release gate additionally uses GCC for eight native C recompilations. Core per-pack CLI/MCP numerical operation does not require GCC, NumPy, SciPy or Fortran. Dependency availability is required for installation, not calculation.

On systems without GCC the root native-rerun tests explicitly skip; do not report them as passed there. The delivered gate ran them all with no skips. CLI alarm enforcement is POSIX/Linux, and these artifacts were tested on Linux.

Each pack can be copied independently with its LICENSE/NOTICE and upstream evidence. The adaptation adds no license restrictions beyond the preserved original BSD terms. Every MCP server is stdio-only with exactly one bounded math tool; no HTTP listener is started.

The archive is reproducibly generated without caches, temporary shared libraries or user/group identities. FILES.sha256 inside each pack checks its own artifacts. Outer SHA256SUMS checks the archive and companion delivery files; it is intentionally outside the archive. If 8 MiB splitting is necessary, concatenate parts in lexical order before checking the reconstructed archive hash.

SHA-256 is an integrity check, not publisher authentication. Follow the source-specific numerical/time-scale limitations and human-review guidance; no independent certification is implied.
