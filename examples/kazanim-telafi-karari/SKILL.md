---
name: kazanim-telafi-karari
description: After a quiz or exam question on one learning objective, decides the next
  teaching step for the class. Uses class size, number of students who answered
  correctly and the most common error type to choose between moving on, small-group
  remediation, rewording the question, or reteaching. Use when a teacher asks what to
  do after quiz results or whether a learning objective needs remediation.
license: Apache-2.0
compatibility: Requires a skillpack runtime that supports flow profile 0.1.
metadata:
  skillpack-spec: "0.1-taslak"
  skillpack-manifest: "skillpack.yaml"
---
# Remediation decision for one learning objective

Do not decide yourself. Run `flow.yaml` with the skillpack runtime and report its
outcome message unchanged.

Rules the flow applies, in order:

1. If more students answered correctly than are in the class, the numbers are wrong.
2. Compute the success percentage.
3. At or above `mastery_pct`: move on.
4. Below `reteach_pct`: reteach; with a different approach if the common error is a
   misconception.
5. In between: reword the question if students did not understand it, otherwise
   remediate in a small group.

Percentages are illustrative. The teacher sets them.
