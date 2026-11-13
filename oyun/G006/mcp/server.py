#!/usr/bin/env python3
"""Single deterministic local tool, official FastMCP, stdio only. Never logs tool arguments."""
import asyncio,json,logging,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tool"))
from runtime import validate,fail,TIMEOUT
from mcp import types
from mcp.server.fastmcp import FastMCP
META=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
NAME=META["mcp"]["tool_name"]
OUTPUT_LIMIT=2097152

def result(v):
    return types.CallToolResult(content=[types.TextContent(type="text",text=json.dumps(v,allow_nan=False,ensure_ascii=False))],structuredContent=v,isError=not v.get("ok",False))

class Server(FastMCP):
    def __init__(self):
        super().__init__(META["mcp"]["server_name"],instructions=META["mcp"]["instructions"],log_level="ERROR")
        self.gate=asyncio.Semaphore(1)
    async def list_tools(self):
        return [types.Tool(name=NAME,description=META["description"],inputSchema=META["inputs"],annotations=types.ToolAnnotations(readOnlyHint=META["mcp"]["read_only"],destructiveHint=False,idempotentHint=META["mcp"]["read_only"],openWorldHint=False))]
    async def call_tool(self,name,arguments):
        if name!=NAME:return result(fail("Unknown tool","UNKNOWN_TOOL"))
        try:validate(arguments)
        except Exception as e:return result(fail(e))
        async with self.gate:
            proc=None
            try:
                proc=await asyncio.create_subprocess_exec(sys.executable,str(ROOT/"tool"/"main.py"),stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
                out,err=await asyncio.wait_for(proc.communicate(json.dumps(arguments,allow_nan=False,separators=(",",":"),ensure_ascii=False).encode()),timeout=TIMEOUT)
                if len(out)>OUTPUT_LIMIT:return result(fail("Output too large","OUTPUT_LIMIT"))
                return result(json.loads(out.decode("utf-8")))
            except asyncio.TimeoutError:return result(fail("Calculation exceeded %d seconds"%TIMEOUT,"TIMEOUT"))
            except Exception as e:return result(fail(type(e).__name__,"EXECUTION_ERROR"))
            finally:
                if proc is not None and proc.returncode is None:
                    proc.kill();await proc.wait()
if __name__=="__main__":
    if len(sys.argv)!=1:raise SystemExit("stdio only; no arguments accepted")
    logging.disable(logging.WARNING)
    Server().run(transport="stdio")
