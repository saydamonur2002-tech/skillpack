import asyncio,json,sys,subprocess,time,importlib.util
from pathlib import Path
import pytest
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1]
PACKS=sorted(ROOT.glob('M[0-9][0-9][0-9]'))

@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_real_stdio_protocol(pack):
    async def run():
        manifest=json.loads((pack/'manifest.json').read_text());example=json.loads((pack/'example.json').read_text());name=manifest['mcp']['tool_name']
        async with stdio_client(StdioServerParameters(command=sys.executable,args=[str(pack/'mcp'/'server.py')])) as (reader,writer):
            async with ClientSession(reader,writer) as session:
                await session.initialize();tools=(await session.list_tools()).tools
                assert len(tools)==1;assert tools[0].name==name;assert tools[0].inputSchema==manifest['inputs']
                good=await session.call_tool(name,example);assert not good.isError;assert good.structuredContent['ok'] is True
                bad=await session.call_tool(name,{});assert bad.isError;assert bad.structuredContent['ok'] is False
                unknown=await session.call_tool('not_exposed',example);assert unknown.isError
                assert unknown.structuredContent['error']['code']=='UNKNOWN_TOOL'
    asyncio.run(run())

def test_real_cli_ten_second_watchdog():
    pack=PACKS[0];example=(pack/'example.json').read_bytes()
    code='import sys,time;sys.path.insert(0,'+repr(str(pack/'tool'))+');from runtime import cli;sys.exit(cli(lambda _: time.sleep(11)))'
    started=time.monotonic();proc=subprocess.run([sys.executable,'-c',code],input=example,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=13)
    elapsed=time.monotonic()-started;out=json.loads(proc.stdout)
    assert proc.returncode==2;assert out['error']['code']=='TIMEOUT';assert 9.5<=elapsed<=12

def test_mcp_timeout_kills_child(monkeypatch):
    # Exercise the actual kill/reap branch with a shortened test-only wait.
    # The production constant remains 10 and is separately asserted per pack.
    pack=PACKS[0];spec=importlib.util.spec_from_file_location('timeout_test_server',pack/'mcp'/'server.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    real_create=asyncio.create_subprocess_exec;real_wait=asyncio.wait_for;children=[]
    async def create(*args,**kwargs):
        proc=await real_create(sys.executable,'-c','import time;time.sleep(30)',**kwargs);children.append(proc);return proc
    async def wait(awaitable,timeout):
        assert timeout==10
        return await real_wait(awaitable,timeout=.05)
    monkeypatch.setattr(module.asyncio,'create_subprocess_exec',create);monkeypatch.setattr(module.asyncio,'wait_for',wait)
    async def run():
        server=module.Server();example=json.loads((pack/'example.json').read_text());reply=await server.call_tool(module.NAME,example)
        assert reply.isError;assert reply.structuredContent['error']['code']=='TIMEOUT'
        assert len(children)==1;assert children[0].returncode is not None
    asyncio.run(run())
