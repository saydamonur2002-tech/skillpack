import copy
import tempfile
import unittest
from pathlib import Path

from skillpack.flow import FlowError, coerce, fmt, run
from skillpack.host import ScriptedHost
from skillpack.pack import check_flow, load_pack, validate_pack

from .helpers import FLOW, MANIFEST, write_pack


class CoerceTest(unittest.TestCase):
    def test_number(self):
        spec = {"type": "number", "min": 0, "max": 10}
        self.assertEqual(coerce(spec, "6,5"), 6.5)
        self.assertEqual(coerce(spec, 3), 3.0)
        for bad in ["on", "11", "-1", True, "nan", "inf", None]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                coerce(spec, bad)

    def test_integer(self):
        self.assertEqual(coerce({"type": "integer"}, "4"), 4)
        with self.assertRaises(ValueError):
            coerce({"type": "integer"}, "4.5")

    def test_bool(self):
        spec = {"type": "bool"}
        self.assertIs(coerce(spec, "Evet"), True)
        self.assertIs(coerce(spec, "hayır"), False)
        self.assertIs(coerce(spec, False), False)
        with self.assertRaises(ValueError):
            coerce(spec, "belki")

    def test_choice(self):
        spec = {"type": "choice", "choices": ["a", "b"]}
        self.assertEqual(coerce(spec, "B"), "b")
        self.assertEqual(coerce(spec, "1"), "a")
        with self.assertRaises(ValueError):
            coerce(spec, "3")

    def test_fmt(self):
        self.assertEqual(fmt(6.5), "6,5")
        self.assertEqual(fmt(2.0), "2")
        self.assertEqual(fmt(True), "evet")


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def pack(self, **kwargs):
        return load_pack(write_pack(self.root, **kwargs))

    def test_same_input_same_result(self):
        pack = self.pack()
        first = run(pack, ScriptedHost({"olcum": 12})).to_dict()
        second = run(pack, ScriptedHost({"olcum": 12})).to_dict()
        self.assertEqual(first, second)
        self.assertEqual(first["outcome"], "yuksek")
        self.assertEqual(first["message"], "Yüksek: 12, fark 2")

    def test_unknown_answer_escalates(self):
        result = run(self.pack(), ScriptedHost({}))
        self.assertEqual(result.verdict, "escalate")
        self.assertEqual(result.message, "Cevapsız: Ölçüm?")

    def test_invalid_answer_is_never_used(self):
        host = ScriptedHost({"olcum": "çok"})
        result = run(self.pack(), host)
        self.assertEqual(result.verdict, "escalate")
        self.assertEqual(len(host.asked), 3)

    def test_action_needs_human_approval(self):
        pack = self.pack()
        approved = ScriptedHost({"olcum": 12}, confirm=True)
        result = run(pack, approved)
        self.assertEqual(approved.performed, [("record", "Yüksek: 12")])
        self.assertEqual(len(result.performed), 1)

        declined = ScriptedHost({"olcum": 12}, confirm=False)
        result = run(pack, declined)
        self.assertEqual(declined.performed, [])
        self.assertEqual(result.suggested, [{"action": "record", "text": "Yüksek: 12"}])

    def test_suggest_mode_never_acts(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["human_in_loop"]["mode"] = "suggest"
        host = ScriptedHost({"olcum": 12}, confirm=True)
        result = run(self.pack(manifest=manifest), host)
        self.assertEqual(host.performed, [])
        self.assertEqual(host.confirmed, [])
        self.assertEqual(len(result.suggested), 1)

    def test_model_value_is_confirmed_by_human(self):
        pack = self.pack()
        host = ScriptedHost({}, confirm=True)
        result = run(pack, host, prefilled={"olcum": 4}, prefilled_source="model")
        self.assertEqual(result.outcome, "uygun")
        self.assertEqual(host.asked, [])
        self.assertIn("Doğru mu?", host.confirmed[0])
        self.assertEqual(result.trace[0]["source"], "model+onay")

    def test_rejected_model_value_falls_back_to_human(self):
        host = ScriptedHost({"olcum": 12}, confirm=False)
        result = run(self.pack(), host, prefilled={"olcum": 4}, prefilled_source="model")
        self.assertEqual(host.asked, ["olcum"])
        self.assertEqual(result.values["olcum"], 12)

    def test_out_of_range_model_value_is_dropped(self):
        host = ScriptedHost({"olcum": 5})
        result = run(self.pack(), host, prefilled={"olcum": 5000}, prefilled_source="model")
        self.assertEqual(host.confirmed, [])
        self.assertEqual(result.values["olcum"], 5)

    def test_sensor_before_human(self):
        flow = copy.deepcopy(FLOW)
        flow["inputs"]["olcum"]["sensor"] = "basinc"
        manifest = copy.deepcopy(MANIFEST)
        manifest["capabilities"]["sensors"] = ["basinc"]
        host = ScriptedHost({}, sensors={"basinc": 3})
        result = run(self.pack(manifest=manifest, flow=flow), host)
        self.assertEqual(host.asked, [])
        self.assertEqual(result.trace[0]["source"], "sensör")

    def test_loop_is_bounded(self):
        flow = copy.deepcopy(FLOW)
        flow["steps"] = [
            {"id": "a", "decide": [{"else": True, "goto": "a"}]},
        ]
        with self.assertRaises(FlowError):
            run(self.pack(flow=flow), ScriptedHost({}))


class CheckFlowTest(unittest.TestCase):
    def errors(self, mutate):
        flow = copy.deepcopy(FLOW)
        manifest = copy.deepcopy(MANIFEST)
        mutate(flow, manifest)
        return check_flow(flow, manifest)

    def test_valid(self):
        self.assertEqual(self.errors(lambda f, m: None), [])

    def test_undeclared_action(self):
        errors = self.errors(lambda f, m: m["capabilities"].update(tools=[]))
        self.assertTrue(any("beyan edilmemiş" in e for e in errors))

    def test_unknown_tool(self):
        errors = self.errors(lambda f, m: m["capabilities"].update(tools=["host:record", "host:shell"]))
        self.assertTrue(any("bilinmeyen araç" in e for e in errors))

    def test_undefined_name_in_expression(self):
        errors = self.errors(lambda f, m: f["steps"][1]["compute"].update(fark="olcum - yok"))
        self.assertTrue(any("tanımsız ad 'yok'" in e for e in errors))

    def test_unsafe_expression(self):
        errors = self.errors(lambda f, m: f["steps"][1]["compute"].update(fark="olcum.real"))
        self.assertTrue(any("desteklenmeyen" in e for e in errors))

    def test_decide_needs_else(self):
        errors = self.errors(lambda f, m: f["steps"][2]["decide"].pop())
        self.assertTrue(any("else olmalı" in e for e in errors))

    def test_bad_goto_and_outcome(self):
        def mutate(f, m):
            f["steps"][2]["decide"][0]["goto"] = "olmayan"
            f["steps"][4]["finish"] = "olmayan"
        errors = self.errors(mutate)
        self.assertTrue(any("tanımsız adım" in e for e in errors))
        self.assertTrue(any("tanımsız sonuç" in e for e in errors))

    def test_must_not_fall_off_the_end(self):
        errors = self.errors(lambda f, m: f["steps"].pop())
        self.assertTrue(any("son adım" in e for e in errors))

    def test_on_unknown_must_escalate(self):
        errors = self.errors(lambda f, m: f.update(on_unknown="uygun"))
        self.assertTrue(any("escalate" in e for e in errors))

    def test_placeholder(self):
        errors = self.errors(lambda f, m: f["outcomes"]["uygun"].update(message="{olmayan}"))
        self.assertTrue(any("yer tutucu" in e for e in errors))

    def test_undeclared_sensor(self):
        errors = self.errors(lambda f, m: f["inputs"]["olcum"].update(sensor="gizli"))
        self.assertTrue(any("sensör" in e for e in errors))


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_valid_pack(self):
        _, report = validate_pack(write_pack(self.root))
        self.assertEqual(report.errors, [])

    def test_raw_customer_data_must_be_false(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["privacy"]["raw_customer_data"] = True
        _, report = validate_pack(write_pack(self.root, manifest=manifest))
        self.assertFalse(report.ok)

    def test_network_and_cloud_are_refused(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["capabilities"]["network"] = "allowlist"
        manifest["capabilities"]["cloud_egress"]["allowed"] = True
        _, report = validate_pack(write_pack(self.root, manifest=manifest))
        self.assertEqual(len([e for e in report.errors if "capabilities" in e]), 2)

    def test_approval_for_this_version_required(self):
        path = write_pack(self.root)
        (path / "provenance" / "approvals.json").write_text('{"approvals": []}', "utf-8")
        _, report = validate_pack(path)
        self.assertTrue(any("insan onayı" in e for e in report.errors))

    def test_directory_name_must_match(self):
        path = write_pack(self.root)
        renamed = path.rename(self.root / "baska-ad")
        _, report = validate_pack(renamed)
        self.assertTrue(any("dizin adı" in e for e in report.errors))

    def test_unknown_field_is_warning(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["gelecek_alan"] = 1
        _, report = validate_pack(write_pack(self.root, manifest=manifest))
        self.assertTrue(report.ok)
        self.assertTrue(any("gelecek_alan" in w for w in report.warnings))

    def test_pii_warning(self):
        path = write_pack(self.root)
        (path / "notlar.md").write_text("ulaşın: biri@example.com", "utf-8")
        _, report = validate_pack(path)
        self.assertTrue(any("e-posta" in w for w in report.warnings))

    def test_flow_path_cannot_escape_pack(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["components"]["flow"] = "../flow.yaml"
        path = write_pack(self.root, manifest=manifest)
        (self.root / "flow.yaml").write_text("flow: '0.1'", "utf-8")
        _, report = validate_pack(path)
        self.assertTrue(any("paket dışına" in e for e in report.errors))


if __name__ == "__main__":
    unittest.main()
