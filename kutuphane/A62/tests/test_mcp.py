"""Real stdio MCP checks using the existing known-answer vectors."""
from pathlib import Path
import sys
PACK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK.parent / "_mcp"))
from mcp_checks import check_pack

def test_mcp_stdio_contract():
    check_pack(PACK)
