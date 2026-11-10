---
name: rulman-isi-titresim
description: Shift-start health check for an electric motor or pump bearing in a factory.
  Uses bearing temperature, ambient temperature, vibration velocity and abnormal noise to
  decide whether to keep running, monitor, lubricate, or stop the machine and call
  maintenance. Use when someone asks about a hot, noisy or vibrating bearing or motor.
license: Apache-2.0
compatibility: Requires a skillpack runtime that supports flow profile 0.1.
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
---
# Bearing temperature and vibration check

Do not decide yourself. Run `flow.yaml` with the skillpack runtime and report its
outcome message unchanged. The runtime asks the operator for each measurement.

Rules the flow applies, in order:

1. Stop if the bearing is at or above `temp_stop_c`, or `delta_stop_c` above ambient,
   or vibration is at or above `vib_stop_mm_s`.
2. Otherwise, if temperature rise or vibration reaches the warning limits, or the
   operator hears abnormal noise, ask whether lubrication is on schedule: lubricate if
   not, monitor if yes.
3. Otherwise the bearing is fine.

Threshold values are illustrative and live in `flow.yaml` under `params`.
