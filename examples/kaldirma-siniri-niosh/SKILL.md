---
name: kaldirma-siniri-niosh
description: Computes the recommended weight limit and lifting index for a two-handed manual
  lift with the Revised NIOSH Lifting Equation (NIOSH 94-110), from hand position, travel
  distance, twist angle, frequency, duration and grip quality. Use when someone asks whether
  a load is safe to lift by hand or how heavy a box a worker may lift.
license: Apache-2.0
compatibility: Requires a skillpack runtime that supports flow profile 0.1 with hazards.
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
---
# Manual lifting limit (Revised NIOSH Lifting Equation)

Do not decide or calculate yourself. Run `flow.yaml` with the skillpack runtime and report
its outcome message unchanged. The runtime asks for each measurement.

What the flow does:

1. Stops at once if the hands are more than 63 cm from the ankles, higher than 175 cm, or
   the trunk twists more than 135 degrees: the recommended limit is zero.
2. Computes the horizontal, vertical, distance and asymmetry multipliers.
3. Reads the frequency multiplier (Table 5) and the coupling multiplier (Table 7).
4. Computes the recommended weight limit and the lifting index (load divided by limit).
5. Index up to 1: acceptable. Above 1: increased risk. Above 3: do not lift by hand.

All numbers come from the NIOSH manual; see `provenance/KAYNAK.md` for the source, the
deviations from it and the comparison with the manual's own worked examples.
