# Learning path: Wanted level (0-5 stars) and police response rules

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Heat to stars
Add 85 heat by hand and count thresholds reached: 2 stars.

## 2. Cooldown
With 2 stars the cooldown is 12 s: replay a 15 s tick and compute 3 s of decay.

## 3. Paint shop
Explain why the paint shop refuses while police are watching.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: the heat per crime, the star thresholds, cooldowns and police numbers: is escaping 1-2 stars easy and 5 stars hard but possible?
