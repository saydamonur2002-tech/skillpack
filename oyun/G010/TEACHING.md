# Learning path: Save and load game state (versioned JSON envelope with FNV-1a checksum)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Canonical JSON
Sort the keys of a small state by hand and compare with canonical_state.

## 2. Checksum
Change one digit in a saved envelope and load it: valid becomes false.

## 3. Versions
Explain why a version number is stored even though only version 1 exists.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that every field the game needs to resume is in the state and that an old save is refused politely rather than crashing.
