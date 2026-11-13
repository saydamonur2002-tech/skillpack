#!/usr/bin/env python3
"""Expose this existing local pack through the official MCP SDK over stdio."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "_mcp"))
from skillpack_runtime import run_single
if __name__ == "__main__":
    run_single(Path(__file__).resolve().parents[1].name)
