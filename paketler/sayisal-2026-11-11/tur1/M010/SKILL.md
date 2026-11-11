---
name: m010
description: "Constructs combinatorial D-W or normalized graph Laplacians from a finite nonnegative weighted adjacency matrix, averaging directed edges and preserving upstream isolated-node semantics."
---

# Weighted graph combinatorial and normalized Laplacians

Use this pack only for the exact deterministic operation described by manifest.json. Never supply guessed measurements or silently coerce strings/booleans into numbers.

## Contract

Constructs combinatorial D-W or normalized graph Laplacians from a finite nonnegative weighted adjacency matrix, averaging directed edges and preserving upstream isolated-node semantics.

Read manifest.json for the strict JSON schema. Additional fields, nonfinite numbers and duplicate JSON keys are rejected. Exactly one request object is read from stdin and one JSON result is written to stdout. Success is `{ "ok": true, "result": {...} }`; failure is `{ "ok": false, "error": {"code": "...", "message": "..."} }` and CLI exit code 2.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tool/main.py < example.json
```

Dependency installation needs package availability; dependencies are not bundled. Calculations require no network access once installed.

## MCP connection

```json
{
  "mcpServers": {
    "m010": {
      "command": "/ABSOLUTE/PATH/TO/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/M010/mcp/server.py"
      ]
    }
  }
}
```

The official FastMCP server exposes exactly `skillpack_m010` over stdio only. It validates the advertised schema and argument JSON (64 KiB UTF-8 ceiling), executes one fixed local script, and kills it after 10 seconds. It has no file-path, shell-code or network parameters. This is a bounded calculator, not a security sandbox for hostile code. The hosting AI client's own privacy settings are outside this pack's control.

## Limits and human review

Square nonnegative dense matrix of 1..32 vertices. Directed input is deliberately averaged with its transpose: this loses orientation. No graph inference, eigensolver, Fourier basis, negative-edge model or graph learning. Self-loop handling follows D-W / normalized formula.

Ports Graph.compute_laplacian combinatorial and normalized formulas using dense Python lists, with directed mean-symmetrization and zero normalized diagonal for isolated vertices. Weighted degrees come from the symmetrized matrix.

Do not present model explanations as independent evidence. Cite SOURCE.md, preserve the input units and precision, and ask a human to review consequential decisions. Teaching steps are in TEACHING.md. The source licenses and original upstream copyright notices must travel with redistributions. This adaptation and its documentation were generated with AI; no upstream endorsement or independent certification is implied.
