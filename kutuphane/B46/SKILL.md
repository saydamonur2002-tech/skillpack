---
name: b46
description: Home Assistant motion-light offline replay
---
# Home Assistant motion-light offline replay
Use this pack only for its declared narrow deterministic computation.

Call `python3 tool/main.py` from this pack directory and supply one JSON object on stdin. It emits one JSON response with `ok` and `result`, or an explicit `error`. Shared dependencies live in `../_vendor`; JavaScript-backed tools also need `../_node`.

Read `manifest.json` for the exact input schema. Deterministic simulation of restart, wait-for-off and delay. Deadline is processed before an event at the same timestamp; this tie rule is explicit. No lights are operated.

The technique is the tool. The model only explains outputs. A recognized intent or a computed result never authorizes a device action. Signature and revocation fields are placeholders, not trust signals.

Distribution: `public-ok`. Never interpret private-only as public permission.

## MCP interface
Run `python3 mcp/server.py` from this pack directory. Call `skillpack_b46` with the same JSON object as the CLI. The tool advertises the exact manifest input/output schemas and returns the existing result envelope as structured JSON. Invalid inputs return an MCP tool error (`isError: true`). Distribution: `public-ok`. See `../_mcp/README.md`.
