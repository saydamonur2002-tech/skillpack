# Control Pipeline Mapping (C01–C11)

This skill provides local subset checks. Full pipeline often requires external tools (agentskills CLI, pinned Ruff, independent oracles).

| Control | Local support | Notes |
|---|---|---|
| C01 | Partial | Check SKILL.md YAML frontmatter presence |
| C02 | Manual | Agent must record SHA / PyPI hash |
| C03 | Partial | Check license file exists and is non-empty |
| C04 | Yes | Run tests/ offline |
| C05 | Partial | Look for origin comments in tests |
| C06 | Manual | Document oracle used |
| C07 | No | Ruff version not pinned here; run externally |
| C08 | Partial | Offer deterministic zip helper |
| C09 | Yes | Static scan for network imports in main.py |
| C10 | Partial | Basic personal info scan |
| C11 | Yes | Record Python version, installed package versions |

When a control is UNAVAILABLE, record it explicitly. Do not claim PASS.

Second environment: copy pack, re-validate, confirm identical zip hash.
