# Learning path: 2D vehicle kinematics (kinematic bicycle model: accelerate, brake, steer)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. The model
Trace one step by hand: x=0,y=0,yaw=0,v=2, a=1, steer 10 deg, L=2.9, dt=0.1. Compute x, yaw and v and compare with the tool.

## 2. Clipping
Ask for 45 deg steering and see that 30 deg is used (max_steer_deg).

## 3. Yaw wrap
Drive a full circle and watch yaw jump from +pi to -pi.

## 4. Game tuning
Use speed_limits and a 0.016 s step to find how long the car needs to reach top speed.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: that wheelbase, steering limit, acceleration, braking and top speed feel right for the city scale and that the car can take a corner on a 2-tile road.
