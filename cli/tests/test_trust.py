"""İmzalı iptal listesi (TUF) ve kurulum kaydı (geri sarma, yayıncı değişimi)."""

import copy
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from skillpack.registry import Registry
from skillpack.signing import generate_key, sign_pack, verify_pack
from skillpack.state import InstallState

from .helpers import MANIFEST, write_pack

try:
    import tuf  # noqa: F401
    from skillpack import revocation
    HAVE_TUF = True
except ImportError:  # pragma: no cover
    HAVE_TUF = False


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.packs = self.root / "packs"
        self.trust = self.root / "trust"
        self.key = self.root / "key.pem"
        self.key_id = generate_key(self.key, self.trust)
        self.pack = write_pack(self.packs)
        self.pack_id = sign_pack(self.pack, self.key)["pack_id"]


@unittest.skipUnless(HAVE_TUF, "python-tuf kurulu değil")
class SignedRevocationTest(Base):
    def setUp(self):
        super().setUp()
        self.repo = self.root / "iptal-deposu"
        self.keys = self.root / "iptal-anahtarlari"
        self.cache = self.root / "onbellek"
        summary = revocation.publish(self.repo, self.keys)
        self.trusted_root = self.root / "guven-koku.json"
        shutil.copyfile(summary["trusted_root"], self.trusted_root)

    def sync(self):
        return revocation.sync(str(self.repo), self.trusted_root, self.cache)

    def registry(self, **kwargs):
        return Registry(self.packs, self.trust, revocation_cache=self.cache, **kwargs)

    def test_empty_list_lets_the_pack_load(self):
        self.sync()
        self.assertIn("ornek-paket", self.registry().scan().packs)

    def test_published_revocation_reaches_the_client(self):
        self.sync()
        revocation.publish(self.repo, self.keys, [{"pack_id": self.pack_id, "reason": "zararli",
                                                   "date": "2026-11-11"}])
        self.assertIn("ornek-paket", self.registry().scan().packs)  # henüz eşitlenmedi
        self.sync()
        scan = self.registry().scan()
        self.assertEqual(scan.packs, {})
        self.assertIn("paket iptal edilmiş: zararli", scan.rejected[0].reasons)

    def test_key_revocation(self):
        revocation.publish(self.repo, self.keys, [{"key_id": self.key_id, "reason": "guvenlik-acigi",
                                                   "date": "2026-11-11"}])
        self.sync()
        self.assertIn("anahtar iptal", self.registry().scan().rejected[0].reasons[0])

    def test_without_sync_nothing_loads(self):
        scan = self.registry().scan()
        self.assertEqual(scan.packs, {})
        self.assertIn("revocations sync", scan.rejected[0].reasons[0])

    def test_unsigned_edit_of_the_published_list_is_rejected(self):
        revocation.publish(self.repo, self.keys, [{"pack_id": self.pack_id, "reason": "zararli",
                                                   "date": "2026-11-11"}])
        target = self.repo / "targets" / revocation.TARGET
        target.write_text(json.dumps({"revocations": "0.1-taslak", "revoked": []}), "utf-8")
        with self.assertRaises(revocation.RevocationError):
            self.sync()
        self.assertFalse((self.cache / revocation.TARGET).exists())

    def test_rollback_to_an_older_signed_list_is_rejected(self):
        self.sync()
        old = self.root / "eski"
        shutil.copytree(self.repo, old)
        revocation.publish(self.repo, self.keys, [{"pack_id": self.pack_id, "reason": "zararli",
                                                   "date": "2026-11-11"}])
        self.sync()
        shutil.rmtree(self.repo)
        shutil.copytree(old, self.repo)  # saldırgan eski, iptalsiz depoyu sunuyor
        with self.assertRaises(revocation.RevocationError):
            self.sync()
        self.assertEqual(self.registry().scan().packs, {})  # önbellekteki iptal yerinde

    def test_expired_timestamp_is_rejected(self):
        past = datetime.now(timezone.utc) - timedelta(days=30)
        revocation.publish(self.repo, self.keys, timestamp_days=7, now=past)
        with self.assertRaises(revocation.RevocationError) as caught:
            self.sync()
        self.assertIn("Expired", str(caught.exception))

    def test_wrong_trust_root_is_rejected(self):
        other = revocation.publish(self.root / "baska", self.root / "baska-anahtar")
        with self.assertRaises(revocation.RevocationError):
            revocation.sync(str(self.repo), Path(other["trusted_root"]), self.cache)

    def test_stale_cache_blocks_all_packs(self):
        self.sync()
        stamp = self.cache / revocation.STAMP
        data = json.loads(stamp.read_text("utf-8"))
        data["synced_at"] = (datetime.now(timezone.utc) - timedelta(days=20)).isoformat()
        stamp.write_text(json.dumps(data), "utf-8")
        scan = self.registry().scan()
        self.assertEqual(scan.packs, {})
        self.assertIn("bayat", scan.rejected[0].reasons[0])
        self.assertIn("ornek-paket", self.registry(revocation_max_age=None).scan().packs)

    def test_timestamp_refresh_keeps_the_list(self):
        revocation.publish(self.repo, self.keys, [{"pack_id": self.pack_id, "reason": "zararli",
                                                   "date": "2026-11-11"}])
        before = revocation.publish(self.repo, self.keys)
        after = revocation.publish(self.repo, self.keys)
        self.assertEqual(before["list_version"], after["list_version"])
        self.assertEqual(after["timestamp_version"], before["timestamp_version"] + 1)
        self.sync()
        self.assertEqual(self.registry().scan().packs, {})


class InstallStateTest(Base):
    def setUp(self):
        super().setUp()
        self.state = InstallState(self.root / "durum" / "kurulu.json")

    def registry(self):
        return Registry(self.packs, self.trust, state=self.state)

    def republish(self, version, key=None, limit=10):
        shutil.rmtree(self.pack)
        manifest = copy.deepcopy(MANIFEST)
        manifest["version"] = version
        write_pack(self.packs, manifest=manifest)
        flow = self.pack / "flow.yaml"
        flow.write_text(flow.read_text("utf-8").replace("limit: 10", f"limit: {limit}"), "utf-8")
        sign_pack(self.pack, key or self.key)

    def test_first_sight_is_recorded_and_repeat_is_accepted(self):
        self.assertIn("ornek-paket", self.registry().scan().packs)
        self.assertIn("ornek-paket", self.registry().scan().packs)
        self.assertEqual(self.state.entries()["ornek-paket"]["version"], "1.0.0")

    def test_upgrade_is_accepted_then_rollback_is_rejected(self):
        self.registry().scan()
        self.republish("1.1.0")
        self.assertIn("ornek-paket", self.registry().scan().packs)
        self.republish("1.0.0")
        scan = self.registry().scan()
        self.assertEqual(scan.packs, {})
        self.assertIn("geri sarma", scan.rejected[0].reasons[0])
        self.assertTrue(verify_pack(self.pack, self.trust).ok)  # imza tek başına bunu yakalamaz

    def test_same_version_with_different_content_is_rejected(self):
        self.registry().scan()
        self.republish("1.0.0", limit=99)
        self.assertIn("değiştirilemez", self.registry().scan().rejected[0].reasons[0])

    def test_other_trusted_key_cannot_take_over_the_name(self):
        self.registry().scan()
        other = self.root / "baska.pem"
        generate_key(other, self.trust)
        self.republish("2.0.0", key=other)
        self.assertIn("yayıncı anahtarı değişmiş", self.registry().scan().rejected[0].reasons[0])

    def test_forget_allows_a_deliberate_change(self):
        self.registry().scan()
        self.republish("0.9.0")
        self.assertEqual(self.registry().scan().packs, {})
        self.assertTrue(self.state.forget("ornek-paket"))
        self.assertIn("ornek-paket", self.registry().scan().packs)

    def test_corrupt_state_rejects_instead_of_trusting(self):
        self.state.path.parent.mkdir(parents=True)
        self.state.path.write_text("bozuk", "utf-8")
        self.assertEqual(self.registry().scan().packs, {})


if __name__ == "__main__":
    unittest.main()
