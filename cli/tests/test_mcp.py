import asyncio
import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from skillpack.mcp_server import Hub, build_server, input_schema
from skillpack.pack import load_pack
from skillpack.registry import Registry
from skillpack.signing import generate_key, sign_pack

from .helpers import FLOW, MANIFEST, write_pack

try:
    import mcp
    from mcp import types as mcp_types
    from mcp.client.stdio import StdioServerParameters
except ImportError:  # pragma: no cover
    mcp = None


class HubCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.packs = self.root / "packs"
        self.trust = self.root / "trust"
        self.key = self.root / "key.pem"
        generate_key(self.key, self.trust)
        flow = copy.deepcopy(FLOW)
        flow["inputs"]["olcum"]["sensor"] = "basinc"
        flow["inputs"]["tur"] = {"type": "choice", "prompt": "Tür?", "choices": ["a", "b"]}
        manifest = copy.deepcopy(MANIFEST)
        manifest["capabilities"]["sensors"] = ["basinc"]
        self.pack = write_pack(self.packs, manifest=manifest, flow=flow)
        sign_pack(self.pack, self.key)
        self.journal = self.root / "runs.jsonl"
        self.sensor = self.root / "basinc.txt"
        self.hub = Hub(Registry(self.packs, self.trust), {"basinc": self.sensor}, self.journal)


class HubTest(HubCase):
    def test_tool_listing(self):
        (tool,) = self.hub.tools()
        self.assertEqual(tool["name"], "ornek-paket")
        self.assertEqual(tool["title"], "Örnek paket")
        self.assertIn("do not decide yourself", tool["description"])
        schema = tool["inputSchema"]
        self.assertEqual(schema["properties"]["olcum"]["type"], ["number", "null"])
        self.assertEqual(schema["properties"]["olcum"]["maximum"], 100)
        self.assertEqual(schema["properties"]["acil"]["type"], ["boolean", "null"])
        self.assertEqual(schema["properties"]["tur"]["enum"], ["a", "b", None])
        self.assertNotIn("required", schema)
        self.assertEqual(input_schema(load_pack(self.pack)), schema)

    def test_missing_value_returns_the_question_not_a_guess(self):
        outcome = self.hub.call("ornek-paket", {})
        self.assertFalse(outcome.is_error)
        self.assertEqual(outcome.structured["status"], "needs_input")
        self.assertEqual(outcome.structured["ask"]["name"], "olcum")
        self.assertEqual(outcome.structured["ask"]["unit"], "bar")
        self.assertIn("INPUT REQUIRED: olcum", outcome.text)
        self.assertIn("Ölçüm? (bar)", outcome.text)
        self.assertFalse(self.journal.exists())

    def test_complete_call_is_deterministic_and_journaled(self):
        first = self.hub.call("ornek-paket", {"olcum": 12})
        second = self.hub.call("ornek-paket", {"olcum": 12})
        self.assertEqual(first.structured, second.structured)
        self.assertEqual(first.structured["status"], "done")
        self.assertEqual(first.structured["verdict"], "stop")
        self.assertTrue(first.text.startswith("[DUR] Yüksek: 12, fark 2"))
        self.assertIn("Kullanılan değerler: olcum=12 (istemci), fark=2", first.text)
        self.assertEqual(first.structured["unconfirmed_inputs"], ["olcum"])
        entries = [json.loads(line) for line in self.journal.read_text("utf-8").splitlines()]
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["outcome"], "yuksek")
        self.assertEqual(entries[0]["values"], {"olcum": 12.0, "fark": 2.0})

    def test_actions_are_never_performed_over_mcp(self):
        outcome = self.hub.call("ornek-paket", {"olcum": 12})
        self.assertEqual(outcome.structured["performed"], [])
        self.assertEqual(outcome.structured["suggested"], [{"action": "record", "text": "Yüksek: 12"}])
        self.assertIn("Önerilen eylem (yapılmadı)", outcome.text)

    def test_null_means_unknown_and_escalates(self):
        outcome = self.hub.call("ornek-paket", {"olcum": None})
        self.assertEqual(outcome.structured["verdict"], "escalate")
        self.assertTrue(outcome.text.startswith("[USTAYA SOR]"))

    def test_invalid_value_is_rejected_with_reason(self):
        outcome = self.hub.call("ornek-paket", {"olcum": 5000})
        self.assertEqual(outcome.structured["status"], "needs_input")
        self.assertEqual(outcome.structured["rejected"], {"name": "olcum", "reason": "en çok 100 olmalı"})
        self.assertIn("was rejected", outcome.text)

    def test_unknown_argument_and_unknown_pack(self):
        self.assertTrue(self.hub.call("ornek-paket", {"uydurma": 1}).is_error)
        outcome = self.hub.call("olmayan", {})
        self.assertTrue(outcome.is_error)
        self.assertIn("depoda yok", outcome.text)

    def test_bound_application_supplies_the_value(self):
        self.sensor.write_text("3.5\n", "utf-8")
        outcome = self.hub.call("ornek-paket", {})
        self.assertEqual(outcome.structured["status"], "done")
        self.assertEqual(outcome.structured["trace"][0]["source"], "sensör")
        self.assertEqual(outcome.structured["values"]["olcum"], 3.5)
        # Sensör istemcinin (modelin) verdiği değerden önce gelir; ezilen değer ize yazılır.
        overridden = self.hub.call("ornek-paket", {"olcum": 7})
        self.assertEqual(overridden.structured["values"]["olcum"], 3.5)
        self.assertEqual(overridden.structured["sources"]["olcum"], "sensör")
        self.assertIn("yok sayıldı", overridden.text)

    def test_tampered_pack_disappears_and_cannot_be_called(self):
        flow = self.pack / "flow.yaml"
        flow.write_text(flow.read_text("utf-8").replace("limit: 10", "limit: 99"), "utf-8")
        self.assertEqual(self.hub.tools(), [])
        outcome = self.hub.call("ornek-paket", {"olcum": 12})
        self.assertTrue(outcome.is_error)
        self.assertIn("dosya imzadan sonra değişmiş", outcome.text)

    def test_new_pack_appears_without_restart(self):
        second = write_pack(self.packs, name="ikinci-paket")
        sign_pack(second, self.key)
        self.assertEqual([tool["name"] for tool in self.hub.tools()], ["ikinci-paket", "ornek-paket"])


@unittest.skipIf(mcp is None, "mcp SDK kurulu değil")
class McpProtocolTest(HubCase):
    """Sunucuyu resmî MCP istemcisiyle sınar."""

    async def _exercise(self, target):
        async with mcp.Client(target) as client:
            listed = await client.list_tools()
            tool = listed.tools[0]
            question = await client.call_tool("ornek-paket", {})
            done = await client.call_tool("ornek-paket", {"olcum": 12})
            missing = await client.call_tool("olmayan", {})
            return client.server_info.name, tool, question, done, missing

    def _check(self, tool, question, done, missing):
        self.assertEqual(tool.name, "ornek-paket")
        self.assertEqual(tool.input_schema["properties"]["tur"]["enum"], ["a", "b", None])
        self.assertFalse(question.is_error)
        self.assertEqual(question.structured_content["ask"]["name"], "olcum")
        self.assertIn("INPUT REQUIRED", question.content[0].text)
        self.assertEqual(done.structured_content["verdict"], "stop")
        self.assertTrue(done.content[0].text.startswith("[DUR]"))
        self.assertTrue(missing.is_error)

    async def _with_user(self, answer, arguments):
        asked = []

        async def user(context, params):
            asked.append(params.message)
            return answer

        params = build_server(self.hub)
        async with mcp.Client(params, elicitation_callback=user) as client:
            return asked, await client.call_tool("ornek-paket", arguments)

    def test_user_confirms_values_directly(self):
        answer = mcp_types.ElicitResult(action="accept", content={"dogru": True})
        asked, done = asyncio.run(self._with_user(answer, {"olcum": 12}))
        self.assertEqual(len(asked), 1)
        self.assertIn("Ölçüm? → 12 bar", asked[0])
        self.assertTrue(done.structured_content["confirmed_by_user"])
        self.assertNotIn("onaylatılmadı", done.content[0].text)
        (line,) = self.journal.read_text("utf-8").splitlines()
        self.assertTrue(json.loads(line)["confirmed_by_user"])

    def test_user_rejects_values_so_there_is_no_verdict(self):
        for answer in (
            mcp_types.ElicitResult(action="accept", content={"dogru": False}),
            mcp_types.ElicitResult(action="decline"),
            mcp_types.ElicitResult(action="cancel"),
        ):
            with self.subTest(action=answer.action):
                _, result = asyncio.run(self._with_user(answer, {"olcum": 12}))
                self.assertEqual(result.structured_content["status"], "not_confirmed")
                self.assertNotIn("verdict", result.structured_content)
                self.assertIn("VALUES NOT CONFIRMED", result.content[0].text)
        self.assertFalse(self.journal.exists())

    def test_sensor_values_need_no_confirmation(self):
        self.sensor.write_text("12\n", "utf-8")
        answer = mcp_types.ElicitResult(action="decline")
        asked, done = asyncio.run(self._with_user(answer, {}))
        self.assertEqual(asked, [])
        self.assertEqual(done.structured_content["verdict"], "stop")

    def test_client_without_elicitation_gets_a_warning(self):
        async def call():
            async with mcp.Client(build_server(self.hub)) as client:
                return await client.call_tool("ornek-paket", {"olcum": 12})

        done = asyncio.run(call())
        self.assertFalse(done.structured_content["confirmed_by_user"])
        self.assertIn("onaylatılmadı", done.content[0].text)

    def test_in_process(self):
        server_name, *results = asyncio.run(self._exercise(build_server(self.hub)))
        self._check(*results)
        self.assertEqual(server_name, "skillpack")

    def test_over_stdio_subprocess(self):
        cli_dir = str(Path(__file__).resolve().parents[1])
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "skillpack", "serve", "--packs", str(self.packs), "--trust", str(self.trust),
                  "--journal", str(self.journal)],
            env={**os.environ, "PYTHONPATH": cli_dir},
        )
        _, *results = asyncio.run(self._exercise(params))
        self._check(*results)
        self.assertEqual(len(self.journal.read_text("utf-8").splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
