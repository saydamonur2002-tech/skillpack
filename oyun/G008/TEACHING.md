# Learning path: Mission chain validation and mission state machine (goto, deliver, escape, collect)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Order
Write three missions where C requires B and B requires A; validate and read order.

## 2. Distance
Compute by hand whether (5,4.5) is inside radius 1.5 of tile (5,5).

## 3. Failure
Give a 5 s limit and a 6 s tick and read the failure and retry in the log.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that missions are in a sensible order, rewards fit the economy, and time limits are achievable on the generated map.
