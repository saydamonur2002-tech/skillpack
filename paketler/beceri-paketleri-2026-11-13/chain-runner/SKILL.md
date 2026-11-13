---
name: chain-runner
description: "Execute a sequence of skillpacks (a→b→c). Use when you have a directive of ordered packs and want to run them with data flowing from one to the next."
---

# chain-runner

Runs an ordered list of skillpacks. Each pack’s output becomes the next pack’s input unless overridden.

## Input
```json
{
  "user_input": "münchen",
  "steps": [
    {"pack": "idna-encode", "from": "user"},
    {"pack": "some-other-pack", "from": "previous"}
  ]
}
```

## Output
```json
{
  "result": <final output>,
  "trace": [ {"step": 0, "pack": "...", "input": ..., "output": ...}, ... ]
}
```

## Limits
- Packs must exist as `<name>.zip` or an unpacked directory under `/workspace/skillpacks/` (override with env `SKILLPACK_PACKS_DIR`)
- Offline
- Apache-2.0
