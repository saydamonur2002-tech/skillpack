"""Shared real-client integration checks; no mock MCP transport."""
import asyncio
from datetime import timedelta
import json
import math
import os
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_mcp" / "vendor"))
from jsonschema import Draft7Validator
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def equal(actual, expected, pack_id):
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool)
        assert math.isclose(actual, expected, rel_tol=1e-6, abs_tol=0.01 if pack_id == "B100" else 1e-8)
    elif isinstance(expected, dict):
        assert isinstance(actual, dict) and set(actual) == set(expected)
        for key in expected:
            equal(actual[key], expected[key], pack_id)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected)
        for a, b in zip(actual, expected):
            equal(a, b, pack_id)
    else:
        assert actual == expected


def server_parameters(path, args=(), env=None):
    clean = {"PATH": os.environ.get("PATH", os.defpath), "PYTHONNOUSERSITE": "1",
             "PYTHONDONTWRITEBYTECODE": "1", "SKILLPACK_DISTRIBUTION": "all"}
    if env:
        clean.update(env)
    return StdioServerParameters(command=sys.executable, args=[str(path), *args], env=clean, cwd=str(ROOT))


async def check_calls(session, pack):
    manifest = json.loads((pack / "manifest.json").read_text())
    name = manifest["mcp"]["tool_name"]
    vectors = json.loads((pack / "tests/vectors.json").read_text())
    vector = next(v for v in vectors if not v.get("error"))
    invalid = dict(vector["input"], __mcp_invalid_input__=True)
    assert not Draft7Validator(manifest["inputs"]).is_valid(invalid)
    bad = await session.call_tool(name, invalid)
    assert bad.isError is True
    assert bad.structuredContent["ok"] is False
    assert bad.structuredContent["error"]["code"] == "INVALID_INPUT"
    Draft7Validator(manifest["outputs"]).validate(bad.structuredContent)
    result = await session.call_tool(name, vector["input"])
    assert result.isError is False, result
    assert result.structuredContent["ok"] is True
    equal(result.structuredContent["result"], vector["result"], pack.name)
    Draft7Validator(manifest["outputs"]).validate(result.structuredContent)
    assert json.loads(result.content[0].text) == result.structuredContent


async def _check_pack(pack):
    manifest = json.loads((pack / "manifest.json").read_text())
    async with stdio_client(server_parameters(pack / "mcp/server.py")) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=90)) as session:
            await session.initialize()
            listed = (await session.list_tools()).tools
            assert len(listed) == 1
            tool = listed[0]
            assert tool.name == manifest["mcp"]["tool_name"]
            assert tool.description == manifest["description"]
            assert tool.inputSchema == manifest["inputs"]
            assert tool.outputSchema == manifest["outputs"]
            assert tool.annotations.readOnlyHint is (pack.name != "B85")
            assert tool.meta["distribution"] == manifest["distribution"]
            await check_calls(session, pack)


def check_pack(pack):
    asyncio.run(_check_pack(pack))


async def _check_aggregate(mode):
    args = ["--public-only"] if mode == "flag" else ["--distribution", "public-ok"] if mode == "distribution_flag" else []
    env = {"SKILLPACK_DISTRIBUTION": "public-ok"} if mode == "env" else None
    public = mode != "all"
    manifests = [json.loads(p.read_text()) for p in ROOT.glob("[AB]*/manifest.json")]
    expected = {m["mcp"]["tool_name"]: m for m in manifests if not public or m["distribution"] == "public-ok"}
    assert len(expected) == (56 if public else 75)
    async with stdio_client(server_parameters(ROOT / "_mcp/skillpack_server.py", args, env)) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=90)) as session:
            await session.initialize()
            listed = (await session.list_tools()).tools
            assert {tool.name for tool in listed} == set(expected)
            for tool in listed:
                assert tool.inputSchema == expected[tool.name]["inputs"]
                assert tool.outputSchema == expected[tool.name]["outputs"]
                assert tool.meta["distribution"] == expected[tool.name]["distribution"]
            # Run two unrelated existing techniques through the same aggregate process.
            await check_calls(session, ROOT / "A64")
            await check_calls(session, ROOT / "B108")
            name = next(m["mcp"]["tool_name"] for m in manifests if m["distribution"] == "private-only") if public else "not_a_pack"
            hidden = await session.call_tool(name, {})
            assert hidden.isError is True
            assert hidden.structuredContent["error"]["code"] == "UNKNOWN_TOOL"


def check_aggregate(mode):
    asyncio.run(_check_aggregate(mode))
