# Learning path: Encoded polyline algorithm format encode and decode

## Prerequisites

Basic arithmetic, reading JSON, and patience to trace a small example by hand. Read the input fields and limits in SKILL.md first.

## 1. Scale and round
Multiply 38.5 and -120.2 by 1e5 and round half away from zero. Explain why plain JavaScript Math.round would differ for negatives.

## 2. Delta and zigzag
Take differences from the previous point, double them, and invert negatives with -v-1. Do this for the second point of the upstream example.

## 3. Five-bit chunks
Split the zigzag value into 5-bit groups from the least significant end, OR 0x20 into all but the last, add 63, and map to characters. Compare with _p~iF.

## 4. Decode and verify
Decode the example back and check the original coordinates; then try a truncated string and explain why the pack rejects it.

## Human check

Run `python tool/main.py < example.json` and `pytest tests`. Compare one expected value with the pinned upstream file under upstream/; say whether it is an upstream literal or an upstream-executed value. Explain every returned field and one rejection case. Human review is required for consequential use.
