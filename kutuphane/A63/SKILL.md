---
name: a63
description: Parse explicit ACL inspector
---
# Parse explicit ACL inspector
Use this pack only for its declared narrow deterministic computation.

Call `python3 tool/main.py` from this pack directory and supply one JSON object on stdin. It emits one JSON response with `ok` and `result`, or an explicit `error`. Shared dependencies live in `../_vendor`; JavaScript-backed tools also need `../_node`.

Read `manifest.json` for the exact input schema. Explicit bits only; no public/role union, server policy or effective authorization result.

The technique is the tool. The model only explains outputs. A recognized intent or a computed result never authorizes a device action. Signature and revocation fields are placeholders, not trust signals.

Distribution: `public-ok`. Never interpret private-only as public permission.

## MCP interface
Run `python3 mcp/server.py` from this pack directory. Call `skillpack_a63` with the same JSON object as the CLI. The tool advertises the exact manifest input/output schemas and returns the existing result envelope as structured JSON. Invalid inputs return an MCP tool error (`isError: true`). Distribution: `public-ok`. See `../_mcp/README.md`.
