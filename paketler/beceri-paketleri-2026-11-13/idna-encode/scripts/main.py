#!/usr/bin/env python3
"""Thin wrapper for idna.encode. Offline, single function."""
import json
import sys
import idna

def main():
    raw = sys.stdin.read()
    data = json.loads(raw)
    inp = data.get("input")
    if not isinstance(inp, str):
        raise ValueError("input must be a string")
    # idna.encode returns bytes; we return the ASCII string form
    result = idna.encode(inp).decode("ascii")
    print(json.dumps({"result": result}))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}))
        sys.exit(1)
