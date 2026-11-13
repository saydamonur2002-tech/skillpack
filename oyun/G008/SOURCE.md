# Source and changes: Mission chain validation and mission state machine (goto, deliver, escape, collect)

Original work by Skillpack contributors (MIT). No third-party code.

## Design notes

Original state machine by Skillpack contributors. Order = repeated choice of the first mission (input order) whose prerequisites are done (stable topological order). Time-limit failure resets the mission timer and progress and counts a failure.

## Reference values

tests/references.json cases were derived by hand (distances and sums are written in each origin).
