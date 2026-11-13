# Learning path: NPC steering behaviours: seek, flee, arrive, pursuit (Yuka)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Seek
With max_speed 2 and a target to the right, the desired velocity is (2,0); the steering force is desired minus current.

## 2. Arrive
See the speed fall as the NPC gets closer than deceleration*max_speed.

## 3. Pursuit
Compare pursuit with seek on a moving evader: pursuit aims ahead and closes faster.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that pedestrians stop smoothly at waypoints, flee when the player drives at them, and that police pursuit is challenging but escapable.
