# Learning path: Game economy: wallet, shop catalog and inventory ledger

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Ledger
Replay the first reference case by hand and write the balance after each line.

## 2. Limits
Try to buy a 6th snack and read the reason.

## 3. Atomic batch
Explain when all_or_nothing is the right mode (a shop basket).

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that prices, sell values and mission rewards keep the player motivated (a paint job should cost about two missions).
