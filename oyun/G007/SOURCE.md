# Source and changes: Wanted level (0-5 stars) and police response rules

Original work by Skillpack contributors (MIT). No third-party code.

## Design notes

Original rules by Skillpack contributors, inspired by the general wanted-level idea of open-world games; no game code or data was copied. stars = number of thresholds reached; on decay stars = min(stars, level(heat)). Decay only counts the part of a tick that lies after the cooldown.

## Reference values

tests/references.json cases were derived by hand from the default table (each origin shows the arithmetic).
