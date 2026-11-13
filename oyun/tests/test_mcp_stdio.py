import asyncio,json,sys,subprocess,time,importlib.util
from pathlib import Path
import pytest
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client,get_default_environment
ROOT=Path(__file__).resolve().parents[1]
PACKS=sorted(ROOT.glob('G[0-9][0-9][0-9]'))

def server_env(pack):
    env=get_default_environment()
    if (pack/'tests'/'fixtures').is_dir():env['SKILLPACK_FILES_DIR']=str(pack/'tests'/'fixtures')
    return env

@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_real_stdio_protocol(pack):
    async def run():
        manifest=json.loads((pack/'manifest.json').read_text());example=json.loads((pack/'example.json').read_text());name=manifest['mcp']['tool_name']
        async with stdio_client(StdioServerParameters(command=sys.executable,args=[str(pack/'mcp'/'server.py')],env=server_env(pack))) as (reader,writer):
            async with ClientSession(reader,writer) as session:
                init=await session.initialize();assert init.serverInfo.name==manifest['mcp']['server_name']
                tools=(await session.list_tools()).tools
                assert len(tools)==1;assert tools[0].name==name;assert tools[0].inputSchema==manifest['inputs']
                assert tools[0].annotations.readOnlyHint is True and tools[0].annotations.openWorldHint is False
                good=await session.call_tool(name,example);assert not good.isError,good.structuredContent;assert good.structuredContent['ok'] is True
                bad=await session.call_tool(name,{});assert bad.isError;assert bad.structuredContent['ok'] is False
                oversized=await session.call_tool(name,dict(example,padding='x'*65537));assert oversized.isError
                assert '65536' in oversized.structuredContent['error']['message']
                unknown=await session.call_tool('not_exposed',example);assert unknown.isError
                assert unknown.structuredContent['error']['code']=='UNKNOWN_TOOL'
    asyncio.run(run())

@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_real_cli_ten_second_watchdog(pack):
    example=(pack/'example.json').read_bytes()
    code='import sys,time;sys.path.insert(0,'+repr(str(pack/'tool'))+');from runtime import cli;sys.exit(cli(lambda _: time.sleep(11)))'
    started=time.monotonic();proc=subprocess.run([sys.executable,'-c',code],input=example,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=13,env=server_env(pack))
    elapsed=time.monotonic()-started;out=json.loads(proc.stdout)
    assert proc.returncode==2;assert out['error']['code']=='TIMEOUT';assert 9.5<=elapsed<=12

@pytest.mark.parametrize('pack',PACKS,ids=lambda p:p.name)
def test_mcp_timeout_kills_child(pack,monkeypatch):
    for mod in ('runtime','main'):sys.modules.pop(mod,None)  # each pack ships its own runtime.py
    monkeypatch.setattr(sys,'path',list(sys.path))
    spec=importlib.util.spec_from_file_location('timeout_test_server_'+pack.name,pack/'mcp'/'server.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
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

@pytest.mark.parametrize('pid',['G010','G012'])
def test_server_never_logs_arguments(pid):
    pack=ROOT/pid;example=json.loads((pack/'example.json').read_text())
    async def run():
        log=pack.parent/('.stderr_'+pid+'.log');errlog=open(log,'w+')
        try:
            async with stdio_client(StdioServerParameters(command=sys.executable,args=[str(pack/'mcp'/'server.py')],env=server_env(pack)),errlog=errlog) as (r,w):
                async with ClientSession(r,w) as s:
                    await s.initialize();name=(await s.list_tools()).tools[0].name
                    await s.call_tool(name,example);await s.call_tool(name,dict(example,unexpected='x'))
            errlog.seek(0);text=errlog.read()
        finally:
            errlog.close();log.unlink()
        assert 'ZZQX' not in text and json.dumps(example)[:200] not in text
    asyncio.run(run())
