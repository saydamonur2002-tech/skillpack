---
name: isi-indeksi-nws
description: Computes the heat index (apparent temperature) from air temperature and relative
  humidity with the US National Weather Service equation and classifies it into the NWS
  categories Caution, Extreme Caution, Danger and Extreme Danger. Use when someone asks how
  hot it feels, or whether heat and humidity make outdoor work or activity risky.
license: Apache-2.0
compatibility: Requires a skillpack runtime that supports flow profile 0.1 with sqrt.
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
---
# Heat index (US National Weather Service)

Do not decide or calculate yourself. Run `flow.yaml` with the skillpack runtime and report
its outcome message unchanged. The runtime asks for temperature in Celsius, relative
humidity in percent, and whether the person is in direct sunlight.

What the flow does:

1. Converts the temperature to Fahrenheit, because the NWS equation is written in it.
2. Computes the simple formula and averages it with the temperature. Below 80 °F that is
   the heat index.
3. Otherwise applies the full regression and, where their conditions hold, the low-humidity
   or high-humidity adjustment.
4. Adds 15 °F in direct sunlight (the worst case the source states).
5. Classifies the result into the NWS categories.

This package is not produced or endorsed by the NWS. See `provenance/KAYNAK.md` for the
sources and for the choices the packager made where the source is silent.
