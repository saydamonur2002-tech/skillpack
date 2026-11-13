---
name: skillpack-orchestrator
description: "Create, validate, and distribute offline skill packs as deterministic ZIPs for Grok bots. Use when building packs from open-source functions, checking controls, or syncing ZIP packages between bot server and user Drive."
type: workflow
lifecycle: active
---

# Skillpack Orchestrator — Build and manage offline skill packs for Grok bots

Orchestrates the skillpack system: turn single functions from open-source libraries into small, offline, tested, source-and-license-recorded packages. Ensures packs follow the standard, can be validated, and are stored/called from Grok bot workspaces.

Use this skill when:
- Creating a new skill pack from a library function
- Validating an existing pack against the control pipeline
- Integrating packs into a Grok bot's filesystem and call protocol
- Composing or discovering packs

## Storage model

Packs are stored **as deterministic ZIP files** (not loose directories as the primary form).

```
/workspace/skillpacks/
  <skill-name>.zip          # primary form on bot server
  <skill-name>/             # temporary unpack for editing/testing (optional)
```

- **Bot server**: one copy lives in the bot's workspace under `/workspace/skillpacks/*.zip`.
- **User side**: second copy is transferred to Google Drive (user's Drive). Use Drive as the distribution and backup channel.
- Transfer flow:
  1. Create pack directory → run validation → produce deterministic ZIP.
  2. Upload ZIP to Drive (`google_drive_upload_artifact`).
  3. User downloads from Drive when needed; bot can re-download if required (`google_drive_download_artifact`).
- Deterministic ZIP ensures the same content always produces the same SHA256 (C08).

Call protocol remains the same once unpacked: `python3 scripts/main.py` with stdin/stdout JSON contract. Libraries must be pre-installed on the bot.

See `references/standard.md` and `references/call_contract.md`.

## Core workflows

### 1. Create a skill pack

1. Identify source (PyPI package + exact function, or GitHub blob).
2. Record source: package version, commit/SHA if applicable, full license text.
3. Scaffold:
   ```bash
   python3 /workspace/artifacts/skillpack-orchestrator/scripts/scaffold_pack.py <skill-name> --source "idna==3.17" --function "idna.encode"
   ```
4. Implement thin `scripts/main.py`: import the library, call the single function, no extra logic.
5. Add tests with known vectors (document origin in comments).
6. Write SKILL.md (usage, inputs/outputs, limits) and manifest.json (source, license, truth_level).
7. Run validation (step 2).
8. Produce deterministic ZIP and record SHA256:
   ```bash
   python3 /workspace/artifacts/skillpack-orchestrator/scripts/make_deterministic_zip.py /workspace/skillpacks/<skill-name>
   ```
9. Keep the ZIP on the bot server and upload the identical ZIP to the user's Google Drive.

Truth levels: `bagimsiz` (independent oracle), `kismi`, `sozlesme` (self-tests only). Prefer independent when possible.

### 2. Validate a pack (control pipeline subset)

Run basic checks locally (full C01–C11 may need external tools):

```bash
python3 /workspace/artifacts/skillpack-orchestrator/scripts/validate_pack.py /workspace/skillpacks/<skill-name>
```

Checks performed (maps to C0x where possible):
- Structure presence (SKILL.md, manifest, scripts/main.py)
- No network calls in main.py (simple scan)
- Tests exist and pass offline
- License text present
- Deterministic zip option

For full pipeline (agentskills validate, Ruff version-pinned, independent oracle): document results in the pack and note UNAVAILABLE if tools missing. See `references/controls.md`.

### 3. Integrate and distribute (bot server + user Drive)

1. Produce deterministic ZIP from the finished pack directory (using make_deterministic_zip.py).
2. Keep ZIP on bot server: `/workspace/skillpacks/<skill-name>.zip`.
3. Upload identical ZIP to user's Google Drive (second copy).
4. On bot: unpack only when needed for execution, or call from a temporary extract.
5. Ensure required library is installed in the bot environment.
6. Optional catalog JSON listing ZIP names, SHA256, and descriptions.
7. To call: extract (or use zipfile) and run `scripts/main.py` with the stdin/stdout contract.

## Key rules

- Packs must be offline at runtime (no GitHub fetches).
- Source copy in `references/` is evidence, not the running code (running code uses installed library).
- Do not mix approval (institutional) with correctness (tests).
- One function per pack. Composition is external.
- Record every claim with command + output.

## Resources

- `references/standard.md` — full system description from source document
- `references/controls.md` — C01–C11 mapping and current gaps
- `references/call_contract.md` — exact stdin/stdout protocol
- `scripts/make_deterministic_zip.py` — create reproducible ZIP (fixed timestamps, sorted) + SHA256
- `scripts/scaffold_pack.py` — create skeleton directory
- `scripts/validate_pack.py` — basic local checks

Load references only when needed for detailed rules or examples.
