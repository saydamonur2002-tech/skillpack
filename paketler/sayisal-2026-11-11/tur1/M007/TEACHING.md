# Learning path: Median absolute deviation and Gaussian scale

## Prerequisites

Basic algebra, real-number arrays and JSON; review units and the input/output contract before calculating.

## 1. Sort data and compute the median, including the average of two central values for even lengths.

## 2. Find every absolute distance from that median and take their median.

## 3. Derive why a Gaussian model uses the reciprocal 0.75 normal quantile as scale multiplier.

## 4. Check the upstream cumulative-sum fixture giving MAD 389.5, and construct a mostly repeated vector to explain why MAD zero does not mean every observation is identical.

## Human check

Run `python tool/main.py < example.json`, then `pytest tests`. Open SOURCE.md and compare at least one expected value to the pinned upstream evidence. Explain every returned field and one failure case without asking the model to invent a missing measurement. A human, not a calculator result, approves consequential use.
