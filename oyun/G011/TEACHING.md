# Learning path: Procedural sound effects with ZzFX (horn, crash, siren, pickup, cash, mission, wasted, engine)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Parameters
Read the named field of 'pickup' and change frequency to hear a lower coin.

## 2. Envelope
attack + decay + sustain + release (+ delay) times 44100 gives sample_count; check it for 'crash'.

## 3. Repeatability
Run the same build twice: the checksum is identical because randomness is off.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that each event sound is recognisable, not too loud and not annoying when repeated (siren, engine).
