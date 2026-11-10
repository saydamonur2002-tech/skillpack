import json
import tempfile
import unittest
from pathlib import Path

from skillpack.registry import Registry
from skillpack.signing import SigningError, generate_key, sign_pack, verify_pack

from .helpers import write_pack


class SigningTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.packs = self.root / "packs"
        self.trust = self.root / "trust"
        self.key = self.root / "key.pem"
        self.key_id = generate_key(self.key, self.trust)
        self.pack = write_pack(self.packs)
        self.bundle = sign_pack(self.pack, self.key)

    def verify(self, revocations=None):
        return verify_pack(self.pack, self.trust, revocations)

    def test_signed_pack_verifies(self):
        result = self.verify()
        self.assertTrue(result.ok, result.reasons)
        self.assertEqual(result.pack_id, self.bundle["pack_id"])
        self.assertEqual(result.key_id, self.key_id)

    def test_unsigned_pack(self):
        (self.pack / "skillpack.sig.json").unlink()
        self.assertEqual(self.verify().reasons, ["imza dosyası yok"])

    def test_changed_file(self):
        flow = self.pack / "flow.yaml"
        flow.write_text(flow.read_text("utf-8").replace("limit: 10", "limit: 99"), "utf-8")
        self.assertIn("dosya imzadan sonra değişmiş: flow.yaml", self.verify().reasons)

    def test_added_and_removed_file(self):
        (self.pack / "ek.md").write_text("x", "utf-8")
        (self.pack / "tests" / "cases.yaml").unlink()
        reasons = self.verify().reasons
        self.assertIn("imzalanmamış dosya: ek.md", reasons)
        self.assertIn("imzalı dosya eksik: tests/cases.yaml", reasons)

    def test_attacker_rewrites_checksums(self):
        """Dosyayı değiştirip özetleri de güncellemek imzayı geçersiz kılar."""
        from skillpack.signing import _payload, checksums, pack_id

        flow = self.pack / "flow.yaml"
        flow.write_text(flow.read_text("utf-8").replace("limit: 10", "limit: 99"), "utf-8")
        sums = checksums(self.pack)
        bundle = dict(self.bundle, checksums=sums)
        bundle["pack_id"] = pack_id(_payload(bundle["name"], bundle["version"], sums))
        (self.pack / "skillpack.sig.json").write_text(json.dumps(bundle), "utf-8")
        self.assertEqual(self.verify().reasons, ["imza geçersiz"])

    def test_public_key_cannot_sign(self):
        public = self.trust / f"{self.key_id}.pem"
        with self.assertRaises(SigningError):
            sign_pack(self.pack, public)

    def test_untrusted_key(self):
        other_trust = self.root / "other"
        other_key = self.root / "other.pem"
        generate_key(other_key, other_trust)
        sign_pack(self.pack, other_key)
        result = self.verify()
        self.assertFalse(result.ok)
        self.assertIn("güvenilenler arasında değil", result.reasons[0])

    def test_revoked_pack_and_key(self):
        path = self.root / "revocations.json"
        entry = {"reason": "yanlis-beyan", "date": "2026-11-10"}
        path.write_text(json.dumps({"revocations": "0.1-taslak",
                                    "revoked": [dict(entry, pack_id=self.bundle["pack_id"])]}), "utf-8")
        self.assertIn("paket iptal edilmiş: yanlis-beyan", self.verify(path).reasons)
        path.write_text(json.dumps({"revocations": "0.1-taslak",
                                    "revoked": [dict(entry, key_id=self.key_id)]}), "utf-8")
        self.assertIn("imzalayan anahtar iptal edilmiş: yanlis-beyan", self.verify(path).reasons)
        path.write_text("{bozuk", "utf-8")
        self.assertFalse(self.verify(path).ok)
        path.unlink()
        self.assertFalse(self.verify(path).ok, "verilen iptal listesi yoksa paket yüklenmemeli")

    def test_unsafe_path_and_symlink(self):
        (self.pack / "boşluk var.md").write_text("x", "utf-8")
        with self.assertRaises(SigningError):
            sign_pack(self.pack, self.key)
        (self.pack / "boşluk var.md").unlink()
        (self.pack / "bag").symlink_to(self.key)
        with self.assertRaises(SigningError):
            sign_pack(self.pack, self.key)

    def test_keygen_does_not_overwrite(self):
        with self.assertRaises(SigningError):
            generate_key(self.key, self.trust)

    def test_registry_loads_and_drops_packs_while_running(self):
        registry = Registry(self.packs, self.trust)
        self.assertEqual(sorted(registry.scan().packs), ["ornek-paket"])

        second = write_pack(self.packs, name="ikinci-paket")
        scan = registry.scan()
        self.assertEqual(sorted(scan.packs), ["ornek-paket"])
        self.assertEqual(scan.rejected[0].reasons, ["imza dosyası yok"])

        sign_pack(second, self.key)
        self.assertEqual(sorted(registry.scan().packs), ["ikinci-paket", "ornek-paket"])

        (second / "flow.yaml").write_text("flow: bozuk", "utf-8")
        self.assertEqual(sorted(registry.scan().packs), ["ornek-paket"])


if __name__ == "__main__":
    unittest.main()
