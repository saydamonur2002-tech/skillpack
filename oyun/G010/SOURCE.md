# Source and changes: Save and load game state (versioned JSON envelope with FNV-1a checksum)

Original work by Skillpack contributors (MIT). No third-party code.

## Design notes

Original format by Skillpack contributors. FNV-1a 32 (Fowler-Noll-Vo; offset basis 2166136261, prime 16777619) over the UTF-8 bytes of the canonical JSON. Rounding uses floor(x*1000+0.5)/1000 in both Python and JavaScript, and integral values are written as integers, so Python json and JavaScript JSON.stringify produce the same text.

## Reference values

FNV-1a cases are published test vectors (empty string, 'a', 'foobar'); the canonical form case was written by hand from the rules.
