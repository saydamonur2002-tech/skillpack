"""Exact-schema MCP adapters. All technique logic stays in the existing tools."""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_mcp" / "vendor"))
from jsonschema import Draft7Validator
from mcp import types
from mcp.server.fastmcp import FastMCP


def error_result(code: str, message: str) -> types.CallToolResult:
    value = {"ok": False, "error": {"code": code, "message": message[:400]}}
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=json.dumps(value, allow_nan=False))],
        structuredContent=value,
        isError=True,
    )


class PackTool:
    def __init__(self, path: Path):
        self.path = path.resolve()
        self.manifest = json.loads((path / "manifest.json").read_text())
        self.name = self.manifest["mcp"]["tool_name"]
        self.inputs = Draft7Validator(self.manifest["inputs"])
        self.outputs = Draft7Validator(self.manifest["outputs"])
        Draft7Validator.check_schema(self.manifest["inputs"])
        Draft7Validator.check_schema(self.manifest["outputs"])
        self.module = None

    def describe(self) -> types.Tool:
        m = self.manifest
        # The sandboxed candidate-test runner is not claimed to be read-only.
        read_only = m["id"] != "B85"
        return types.Tool(
            name=self.name,
            title=m["name"],
            description=m["description"],
            inputSchema=m["inputs"],
            outputSchema=m["outputs"],
            annotations=types.ToolAnnotations(
                readOnlyHint=read_only,
                destructiveHint=False,
                idempotentHint=read_only,
                openWorldHint=False,
            ),
            _meta={"skillpack_id": m["id"], "distribution": m["distribution"],
                   "implementation_kind": m["implementation_kind"]},
        )

    def _execute(self, arguments: dict) -> dict:
        # Keep existing imports local and prevent incidental prints from corrupting JSON-RPC.
        # Invocation is synchronous: no concurrent mutation of sys.path/stdout is introduced.
        previous_path = sys.path[:]
        try:
            sys.path.insert(0, str(ROOT / "_vendor"))
            with redirect_stdout(sys.stderr):
                if self.module is None:
                    source = (self.path / self.manifest["tool"]).resolve()
                    if not source.is_relative_to(self.path):
                        raise ValueError("Tool path must remain inside its pack")
                    key = "_skillpack_mcp_tool_" + self.manifest["id"]
                    spec = importlib.util.spec_from_file_location(key, source)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[key] = module
                    try:
                        spec.loader.exec_module(module)
                    except Exception:
                        sys.modules.pop(key, None)
                        raise
                    self.module = module
                data = arguments
                # Reuse the existing Linux probe, not a second implementation of it.
                if arguments.get("probe") is True and self.manifest["id"] in {"B54", "B55"}:
                    if set(arguments) != {"probe"}:
                        raise ValueError("probe cannot be combined with snapshot fields")
                    data = self.module.probe()
                return self.module.handle(data)
        finally:
            sys.path[:] = previous_path

    def invoke(self, arguments: dict) -> types.CallToolResult:
        try:
            raw = json.dumps(arguments, allow_nan=False, ensure_ascii=False).encode("utf-8")
            if len(raw) > self.manifest["budget"]["max_input_bytes"]:
                return error_result("INVALID_INPUT", "Input exceeds the manifest byte budget")
            problem = next(self.inputs.iter_errors(arguments), None)
            if problem is not None:
                return error_result("INVALID_INPUT", problem.message)
        except (TypeError, ValueError, RecursionError) as exc:
            return error_result("INVALID_INPUT", str(exc))
        try:
            output = self._execute(arguments)
            self.outputs.validate(output)
            text = json.dumps(output, allow_nan=False, ensure_ascii=False)
        except Exception as exc:
            return error_result("INVALID_OUTPUT_OR_RUNTIME", str(exc))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=text)],
            structuredContent=output,
            isError=output.get("ok") is not True,
        )


def load_tools(pack_id: str | None = None, distribution: str = "all") -> dict[str, PackTool]:
    if distribution not in {"all", "public-ok"}:
        raise ValueError("Distribution must be all or public-ok")
    paths = sorted(p.parent for p in ROOT.glob("[AB]*/manifest.json")
                   if re.fullmatch(r"[AB][0-9]+", p.parent.name))
    tools = {}
    for path in paths:
        if pack_id is not None and path.name != pack_id:
            continue
        manifest = json.loads((path / "manifest.json").read_text())
        if distribution == "public-ok" and manifest["distribution"] != "public-ok":
            continue
        tool = PackTool(path)
        if tool.name in tools:
            raise ValueError("Duplicate MCP tool name")
        tools[tool.name] = tool
    if pack_id is not None and len(tools) != 1:
        raise ValueError("Requested pack is unavailable in this server")
    return tools


class SkillpackMCP(FastMCP):
    """Override the official FastMCP public handlers to preserve arbitrary JSON Schemas.

    Signature-based schema inference would otherwise change the existing contract.
    FastMCP's normal stdio lifecycle and official protocol handlers remain in use.
    """
    def __init__(self, tools: dict[str, PackTool], title: str = "Local Skillpack"):
        self.pack_tools = tools
        super().__init__(title, instructions=(
            "Call deterministic local tools using their advertised JSON Schemas. "
            "Inspect structuredContent and isError. Respect distribution metadata."
        ))

    async def list_tools(self) -> list[types.Tool]:
        return [tool.describe() for tool in self.pack_tools.values()]

    async def call_tool(self, name: str, arguments: dict) -> types.CallToolResult:
        tool = self.pack_tools.get(name)
        if tool is None:
            return error_result("UNKNOWN_TOOL", "Tool is not exposed by this server")
        return tool.invoke(arguments)


def run_single(pack_id: str) -> None:
    SkillpackMCP(load_tools(pack_id), title="Local Skillpack " + pack_id).run(transport="stdio")


def run_aggregate() -> None:
    parser = argparse.ArgumentParser(description="Expose local packs over MCP stdio")
    parser.add_argument("--public-only", action="store_true", help="Expose public-ok packs only")
    parser.add_argument("--distribution", choices=["all", "public-ok"], default=None)
    args = parser.parse_args()
    distribution = ("public-ok" if args.public_only else
                    args.distribution or os.environ.get("SKILLPACK_DISTRIBUTION", "all"))
    if distribution not in {"all", "public-ok"}:
        parser.error("SKILLPACK_DISTRIBUTION must be all or public-ok")
    SkillpackMCP(load_tools(distribution=distribution)).run(transport="stdio")
