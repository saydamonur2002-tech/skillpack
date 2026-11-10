import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from skillpack.pack import load_pack
from skillpack.router import KeywordRouter, OllamaRouter, normalize

from .helpers import write_pack


class FakeOllama:
    """Ollama /api/chat uç noktasının yerine geçen küçük sunucu."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                outer.requests.append(body)
                reply = outer.replies.pop(0)
                if reply is None:
                    self.send_response(500)
                    self.end_headers()
                    return
                data = json.dumps({"message": {"role": "assistant", "content": reply}}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *args):
                pass

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class RouterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.packs = {
            "ornek-paket": load_pack(write_pack(root)),
        }
        other = load_pack(write_pack(root, name="diger-paket"))
        other.manifest["routing"]["triggers"] = ["ısı", "örnek ölçüm"]
        self.packs["diger-paket"] = other

    def test_normalize_turkish(self):
        self.assertEqual(normalize("ISINIYOR, İyi!"), "ısınıyor iyi")

    def test_keyword_router(self):
        router = KeywordRouter()
        self.assertEqual(router.route("Motor ISINIYOR", self.packs).skill, "diger-paket")
        self.assertIsNone(router.route("hava nasıl", self.packs).skill)
        tie = router.route("örnek ölçüm", self.packs)
        self.assertIsNone(tie.skill)
        self.assertIn("eşit", tie.note)

    def test_model_selects_and_extracts(self):
        fake = FakeOllama(['{"skill": "ornek-paket"}', '{"olcum": 12, "acil": null}'])
        self.addCleanup(fake.close)
        route = OllamaRouter("m", url=fake.url).route("basınç 12 bar", self.packs)
        self.assertEqual((route.skill, route.args, route.source), ("ornek-paket", {"olcum": 12}, "model"))

        select, extract = fake.requests
        self.assertEqual(select["format"]["properties"]["skill"]["enum"],
                         ["diger-paket", "ornek-paket", "none"])
        self.assertEqual(select["options"], {"temperature": 0})
        self.assertFalse(select["stream"])
        self.assertEqual(extract["format"]["properties"]["olcum"], {"type": ["number", "null"]})

    def test_model_says_none(self):
        fake = FakeOllama(['{"skill": "none"}'])
        self.addCleanup(fake.close)
        route = OllamaRouter("m", url=fake.url).route("hava nasıl", self.packs)
        self.assertIsNone(route.skill)
        self.assertEqual(len(fake.requests), 1)

    def test_model_cannot_invent_a_skill_or_field(self):
        fake = FakeOllama(['{"skill": "uydurma"}'])
        self.addCleanup(fake.close)
        self.assertIsNone(OllamaRouter("m", url=fake.url).route("x", self.packs).skill)

        fake2 = FakeOllama(['{"skill": "ornek-paket"}', '{"olcum": 3, "uydurma": 1}'])
        self.addCleanup(fake2.close)
        route = OllamaRouter("m", url=fake2.url).route("x", self.packs)
        self.assertEqual(route.args, {"olcum": 3})

    def test_falls_back_when_model_fails(self):
        for replies in ([None], ["json değil"]):
            fake = FakeOllama(replies)
            self.addCleanup(fake.close)
            route = OllamaRouter("m", url=fake.url).route("ısı yüksek", self.packs)
            self.assertEqual(route.skill, "diger-paket")
            self.assertEqual(route.source, "anahtar-kelime")
            self.assertIn("model kullanılamadı", route.note)

    def test_falls_back_when_server_is_down(self):
        route = OllamaRouter("m", url="http://127.0.0.1:9", timeout=2).route("ısı", self.packs)
        self.assertEqual(route.skill, "diger-paket")


if __name__ == "__main__":
    unittest.main()
