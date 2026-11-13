# Call Contract

Every skill pack must implement this exact interface in `scripts/main.py`.

## Input

Read one JSON object from stdin:

```json
{"input": <any JSON-serializable value>}
```

## Output

Write one JSON object to stdout:

```json
{"result": <any JSON-serializable value>}
```

## Errors

- On failure: write `{"error": "message", "type": "..."}` to stdout (or stderr)
- Exit code != 0

## Rules

- No network
- No side effects outside the function
- Deterministic for same input
- Timeout recommended: 10 seconds
- Max stdin size: 64 KB (enforce if possible)

Example invocation:

```bash
echo '{"input": "xn--nxasmq6b"}' | python3 scripts/main.py
```
