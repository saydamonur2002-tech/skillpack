# Source and changes: Game economy: wallet, shop catalog and inventory ledger

Original work by Skillpack contributors (MIT). No third-party code.

## Design notes

Original ledger by Skillpack contributors. Checks run before any change; all_or_nothing stops at the first rejection and returns the starting wallet and inventory. Money is capped at 1e9.

## Reference values

tests/references.json cases were derived by hand (arithmetic in each origin).
