---
name: soguk-mal-kabul
description: Goods receiving check for chilled and frozen food deliveries in a restaurant
  kitchen. Uses product type, measured core temperature, package condition and days to
  expiry to decide whether to accept, accept conditionally, or reject the delivery. Use
  when a supplier delivery arrives or someone asks whether received food can be accepted.
license: Apache-2.0
compatibility: Requires a skillpack runtime that supports flow profile 0.1.
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
---
# Cold goods receiving

Do not decide yourself. Run `flow.yaml` with the skillpack runtime and report its
outcome message unchanged.

Rules the flow applies, in order:

1. Look up the temperature limit for the product type.
2. Reject if the package is damaged, the product is past its date, a frozen product is
   above its limit, or a chilled product is more than `tolerance_c` above its limit.
3. Accept conditionally (chill now, use today) if a chilled product is above its limit
   but within tolerance.
4. Flag short shelf life if fewer than `min_shelf_days` remain.
5. Otherwise accept.

Limits are illustrative. Replace them with the limits in the kitchen's own food safety
plan before use.
