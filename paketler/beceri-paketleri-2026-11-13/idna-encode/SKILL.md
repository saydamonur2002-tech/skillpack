---
name: idna-encode
description: "Encode a Unicode domain label to ASCII using IDNA 2008 (idna.encode). Use when converting internationalized domain names to punycode/ASCII."
---

# idna-encode

Thin wrapper around `idna.encode`. Returns the ASCII (punycode) form of a domain label or name.

## Input
```json
{"input": "münchen"}
```

## Output
```json
{"result": "xn--mnchen-3ya"}
```

## Limits
- Offline only
- Requires installed library: idna (tested with 3.20)
- Input must be a string
- Follows IDNA 2008 rules (not 2003)
