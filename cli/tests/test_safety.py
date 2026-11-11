"""Güvenlik davranışları: kaynak önceliği, tazelik, tehlike kuralları, katı ifade ve YAML."""

import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from skillpack import expr
from skillpack.flow import FlowError, run
from skillpack.host import Reading, ScriptedHost
from skillpack.pack import PackError, load_pack, strict_load, validate_pack

from .helpers import CASES, FLOW, MANIFEST, write_pack

SENSOR_MANIFEST = copy.deepcopy(MANIFEST)
SENSOR_MANIFEST["capabilities"]["sensors"] = ["basinc"]

HAZARD_FLOW = {
    "flow": "0.1",
    "params": {"limit": 10},
    "inputs": {
        "olcum": {"type": "number", "prompt": "Ölçüm?", "sensor": "basinc", "max_age_s": 60},
        "kacak": {"type": "bool", "prompt": "Kaçak var mı?"},
        "kapak": {"type": "bool", "prompt": "Kapak kapalı mı?"},
    },
    "hazards": [
        {"when": "kacak", "finish": "kacak_var"},
        {"when": "olcum > limit * 2", "finish": "kacak_var"},
    ],
    "steps": [
        {"id": "a", "ask": "kapak"},
        {"id": "b", "ask": "olcum"},
        {"id": "c", "ask": "kacak"},
        {"id": "d", "decide": [
            {"when": "olcum >= limit or not kapak", "finish": "yuksek"},
            {"else": True, "finish": "uygun"},
        ]},
    ],
    "outcomes": {
        "uygun": {"verdict": "ok", "message": "Uygun: {olcum}"},
        "yuksek": {"verdict": "warn", "message": "Yüksek: {olcum}"},
        "kacak_var": {"verdict": "stop", "message": "Durun. Sınır {limit}."},
        "bilinmiyor": {"verdict": "escalate", "message": "Cevapsız: {missing}"},
    },
    "on_unknown": "bilinmiyor",
}

HAZARD_CASES = {
    "cases": [
        {"name": "uygun", "inputs": {"kapak": True, "olcum": 5, "kacak": False}, "expect": {"outcome": "uygun"}},
        {"name": "kaçak", "inputs": {"kapak": True, "olcum": 5, "kacak": True}, "expect": {"outcome": "kacak_var"}},
    ],
    "routing": [{"utterance": "bir örnek ölçüm yapalım"}],
}


class PackCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def pack(self, flow=HAZARD_FLOW, cases=HAZARD_CASES, name="ornek-paket"):
        root = write_pack(self.tmp, name=name, manifest=SENSOR_MANIFEST, flow=flow, cases=cases)
        return load_pack(root)


class SourcePriorityTest(PackCase):
    def test_sensor_beats_client_value(self):
        host = ScriptedHost({"kapak": True, "kacak": False}, sensors={"basinc": Reading(15, age_s=2)})
        result = run(self.pack(), host, prefilled={"olcum": 3}, prefilled_source="istemci")
        self.assertEqual(result.values["olcum"], 15)
        self.assertEqual(result.outcome, "yuksek")
        override = next(entry for entry in result.trace if entry["kind"] == "override")
        self.assertEqual((override["ignored"], override["used"]), (3, 15))

    def test_sensor_beats_model_value_without_asking_for_confirmation(self):
        host = ScriptedHost({"kapak": True, "kacak": False}, sensors={"basinc": Reading(15, age_s=2)})
        result = run(self.pack(), host, prefilled={"olcum": 3}, prefilled_source="model")
        self.assertEqual(result.values["olcum"], 15)
        self.assertEqual(host.confirmed, [])

    def test_stale_reading_is_not_used(self):
        host = ScriptedHost({"kapak": True, "kacak": False, "olcum": 4},
                            sensors={"basinc": Reading(95, age_s=3600)})
        result = run(self.pack(), host)
        self.assertEqual(result.values["olcum"], 4)
        rejected = next(entry for entry in result.trace if entry["kind"] == "sensor")
        self.assertEqual(rejected["reason"], "bayat")

    def test_reading_of_unknown_age_is_not_used_when_freshness_is_declared(self):
        host = ScriptedHost({"kapak": True, "kacak": False, "olcum": 4}, sensors={"basinc": 95})
        self.assertEqual(run(self.pack(), host).values["olcum"], 4)

    def test_reading_without_freshness_limit_is_still_accepted(self):
        flow = copy.deepcopy(HAZARD_FLOW)
        del flow["inputs"]["olcum"]["max_age_s"]
        host = ScriptedHost({"kapak": True, "kacak": False}, sensors={"basinc": 7})
        self.assertEqual(run(self.pack(flow), host).values["olcum"], 7)


class HazardTest(PackCase):
    def test_known_hazard_wins_over_missing_data(self):
        # "kapak" bilinmiyor; eskiden sonuç "bilinmiyor" olurdu.
        host = ScriptedHost({})
        result = run(self.pack(), host, prefilled={"kacak": True}, prefilled_source="istemci")
        self.assertEqual((result.outcome, result.verdict), ("kacak_var", "stop"))
        self.assertEqual(host.asked, [])
        self.assertEqual(result.values, {"kacak": True})

    def test_hazard_from_sensor_fires_before_any_question(self):
        host = ScriptedHost({}, sensors={"basinc": Reading(25, age_s=1)})
        result = run(self.pack(), host)
        self.assertEqual(result.outcome, "kacak_var")
        self.assertEqual(host.asked, [])

    def test_stale_sensor_cannot_trigger_or_hide_a_hazard(self):
        host = ScriptedHost({}, sensors={"basinc": Reading(25, age_s=999)})
        self.assertEqual(run(self.pack(), host).outcome, "bilinmiyor")

    def test_no_hazard_means_normal_flow(self):
        host = ScriptedHost({"kapak": True, "olcum": 5, "kacak": False})
        self.assertEqual(run(self.pack(), host).outcome, "uygun")

    def test_hazard_must_lead_to_stop(self):
        flow = copy.deepcopy(HAZARD_FLOW)
        flow["hazards"][0]["finish"] = "yuksek"
        _, report = validate_pack(self.pack(flow).path)
        self.assertTrue(any("stop" in error for error in report.errors))

    def test_hazard_message_cannot_need_a_value_the_rule_does_not_use(self):
        flow = copy.deepcopy(HAZARD_FLOW)
        flow["outcomes"]["kacak_var"]["message"] = "Durun: {olcum}"
        _, report = validate_pack(self.pack(flow).path)
        self.assertTrue(any("hazards[0]" in error for error in report.errors))

    def test_missing_hazards_is_advice_not_error(self):
        _, report = validate_pack(write_pack(self.tmp, name="ornek-paket"))
        self.assertEqual(report.errors, [])
        self.assertTrue(any("hazards" in line for line in report.advice))


class ValidationTest(PackCase):
    def test_case_without_expectation_is_rejected(self):
        cases = copy.deepcopy(CASES)
        cases["cases"][0]["expect"] = {}
        _, report = validate_pack(write_pack(self.tmp, cases=cases))
        self.assertTrue(any("beklentisiz" in error for error in report.errors))

    def test_condition_must_be_boolean(self):
        flow = copy.deepcopy(FLOW)
        flow["steps"][2]["decide"][0]["when"] = "fark"
        pack = load_pack(write_pack(self.tmp, flow=flow))
        with self.assertRaises(FlowError):
            run(pack, ScriptedHost({"olcum": 5}))


class StrictExprTest(unittest.TestCase):
    def test_types_do_not_mix(self):
        for source in ["'ab' * 3", "1 + true", "x and 5", "'a' == 1", "not 3", "'a' < 'b'",
                       "'et' in s", "[1, 2]", "min(1)", "round(1.5, 9)", "x in [y]"]:
            with self.subTest(source=source):
                with self.assertRaises(expr.ExprError):
                    expr.evaluate(source, {"x": 3, "y": 3, "s": "kirmizi_et"})

    def test_results_are_bounded(self):
        for source in ["999999999999999 * 999999999", "1e300 * 2", "'x' * 300000000"]:
            with self.subTest(source=source):
                with self.assertRaises(expr.ExprError):
                    expr.evaluate(source, {})

    def test_rounding_is_half_up(self):
        self.assertEqual(expr.evaluate("round(2.5)", {}), 3)
        self.assertEqual(expr.evaluate("round(3.5)", {}), 4)
        self.assertEqual(expr.evaluate("round(-2.5)", {}), -3)
        self.assertEqual(expr.evaluate("round(2.675, 2)", {}), 2.68)
        self.assertIs(type(expr.evaluate("round(2.0)", {})), int)

    def test_sqrt(self):
        self.assertEqual(expr.evaluate("sqrt(16)", {}), 4)
        self.assertAlmostEqual(expr.evaluate("sqrt(x) * 2", {"x": 2}), 2.8284271247, places=9)
        self.assertIs(expr.evaluate("sqrt(x)", {}, partial=True), expr.UNKNOWN)
        for source in ["sqrt(-1)", "sqrt('a')", "sqrt(1, 2)"]:
            with self.subTest(source=source):
                with self.assertRaises(expr.ExprError):
                    expr.evaluate(source, {})

    def test_three_valued_logic(self):
        partial = lambda source, env: expr.evaluate(source, env, partial=True)  # noqa: E731
        self.assertIs(partial("a or b", {"a": True}), True)
        self.assertIs(partial("a or b", {"b": True}), True)
        self.assertIs(partial("a or b", {"a": False}), expr.UNKNOWN)
        self.assertIs(partial("a and b", {"a": False}), False)
        self.assertIs(partial("a and b", {"a": True}), expr.UNKNOWN)
        self.assertIs(partial("x > 5 or y < 0", {"y": -1}), True)
        self.assertIs(partial("not a", {}), expr.UNKNOWN)
        self.assertIs(partial("x + 1 > 2", {}), expr.UNKNOWN)
        with self.assertRaises(expr.ExprError):
            expr.evaluate("b or a", {"a": True})


class StrictYamlTest(unittest.TestCase):
    def test_surprising_yaml_11_forms_stay_text(self):
        data = strict_load("sure: 1:30\ncevap: no\nkod: 012\nonay: yes\ntarih: 2026-11-10\n")
        self.assertEqual(data, {"sure": "1:30", "cevap": "no", "kod": "012", "onay": "yes",
                                "tarih": "2026-11-10"})

    def test_plain_values_keep_their_types(self):
        data = strict_load("a: 4\nb: -18\nc: 2.5\nd: true\ne: false\nf: 1e3\ng: metin\nh: ~\n")
        self.assertEqual(data, {"a": 4, "b": -18, "c": 2.5, "d": True, "e": False, "f": 1000.0,
                                "g": "metin", "h": None})

    def test_duplicate_key_is_an_error(self):
        with self.assertRaises(yaml.YAMLError):
            strict_load("limit: 4\nlimit: 40\n")

    def test_duplicate_key_in_flow_rejects_the_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_pack(Path(tmp))
            flow = root / "flow.yaml"
            flow.write_text(flow.read_text("utf-8") + "\non_unknown: uygun\n", "utf-8")
            with self.assertRaises(PackError):
                load_pack(root)


if __name__ == "__main__":
    unittest.main()
