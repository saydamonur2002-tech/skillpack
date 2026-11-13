# Learning path: Fixed-timestep game loop scheduler (MainLoop.js animate)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Accumulator
With a 10 ms step and 33.3 ms frames, predict 3 or 4 updates per frame and check alpha.

## 2. Panic
Feed a 400 ms gap with a 1 ms step and see the loop stop at 240 updates.

## 3. Why fixed steps
Explain why physics should not depend on frame rate (same car path on any screen).

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that the physics step and panic handling match the target devices (phones at 60 Hz, older laptops at 30 Hz).
