"""Depodaki örnek paketlerin ve CLI'nin uçtan uca denetimi."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

from skillpack.cli import main, run_cases
from skillpack.pack import load_cases, validate_pack
from skillpack.registry import Registry
from skillpack.router import KeywordRouter
from skillpack.signing import generate_key

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"
NAMES = [
    "isi-indeksi-nws",
    "kaldirma-siniri-niosh",
    "kazanim-telafi-karari",
    "rulman-isi-titresim",
    "soguk-mal-kabul",
]


class ExamplesTest(unittest.TestCase):
    def test_examples_are_signed_valid_and_loadable(self):
        scan = Registry(EXAMPLES, EXAMPLES / "trust").scan()
        self.assertEqual([(r.path.name, r.reasons) for r in scan.rejected], [])
        self.assertEqual(sorted(scan.packs), NAMES)

    def test_examples_have_no_warnings_and_pass_their_cases(self):
        for name in NAMES:
            with self.subTest(name=name):
                pack, report = validate_pack(EXAMPLES / name)
                self.assertEqual((report.errors, report.warnings), ([], []))  # öneriler (advice) ayrı tutulur
                failed = [(case, detail) for case, ok, detail in run_cases(pack) if not ok]
                self.assertEqual(failed, [])

    def test_routing_examples_reach_their_own_pack(self):
        packs = Registry(EXAMPLES, EXAMPLES / "trust").scan().packs
        router = KeywordRouter()
        for name, pack in packs.items():
            for example in load_cases(pack)["routing"]:
                with self.subTest(utterance=example["utterance"]):
                    self.assertEqual(router.route(example["utterance"], packs).skill, name)


class CliTest(unittest.TestCase):
    def call(self, *argv):
        out = io.StringIO()
        stdin, sys.stdin = sys.stdin, io.StringIO("")  # girdi yok: sorular cevapsız kalır
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                code = main(list(argv))
        finally:
            sys.stdin = stdin
        return code, out.getvalue()

    def test_init_validate_test_sign_verify_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = root / "packs" / "yeni-beceri"
            (root / "packs").mkdir()
            self.assertEqual(self.call("init", str(pack))[0], 0)
            self.assertEqual(self.call("validate", str(pack))[0], 0)
            self.assertEqual(self.call("test", str(pack))[0], 0)

            store = ["--packs", str(root / "packs"), "--trust", str(root / "trust")]
            code, out = self.call("run", "yeni-beceri", "--set", "olcum=3", *store)
            self.assertEqual(code, 1)
            self.assertIn("imza dosyası yok", out)

            key = root / "key.pem"
            self.assertEqual(self.call("keygen", "--out", str(key), "--trust", str(root / "trust"))[0], 0)
            self.assertEqual(self.call("sign", str(pack), "--key", str(key))[0], 0)
            self.assertEqual(self.call("verify", str(pack), "--trust", str(root / "trust"))[0], 0)

            code, out = self.call("run", "yeni-beceri", "--set", "olcum=12", *store)
            self.assertEqual(code, 0)
            self.assertIn("[DİKKAT] Ölçüm 12, sınır 10. Yüksek.", out)

            code, out = self.call("ask", "anahtar sözcük", "--json", *store, )
            self.assertEqual(code, 0)
            self.assertIn('"verdict": "escalate"', out)

    def test_sign_refuses_pack_with_failing_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = root / "yeni-beceri"
            self.call("init", str(pack))
            flow = pack / "flow.yaml"
            flow.write_text(flow.read_text("utf-8").replace("limit: 10", "limit: 3"), "utf-8")
            key = root / "key.pem"
            generate_key(key, root / "trust")
            code, out = self.call("sign", str(pack), "--key", str(key))
            self.assertEqual(code, 1)
            self.assertIn("kabul testleri kaldı", out)
            self.assertFalse((pack / "skillpack.sig.json").exists())


if __name__ == "__main__":
    unittest.main()
