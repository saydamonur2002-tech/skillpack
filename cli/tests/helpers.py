"""Testlerde kullanılan küçük paket üreticisi."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml

MANIFEST = {
    "skillpack": "0.1-taslak",
    "name": "ornek-paket",
    "version": "1.0.0",
    "publisher": {"display": "Test", "org_role": "bireysel"},
    "domain": {"sector": "test", "task": "test", "lang": ["tr"]},
    "components": {"procedure": "SKILL.md", "flow": "flow.yaml", "tests": "tests/cases.yaml"},
    "routing": {"title": "Örnek paket", "triggers": ["örnek ölçüm"]},
    "capabilities": {"tools": ["host:record"], "network": "none", "cloud_egress": {"allowed": False}},
    "human_in_loop": {"mode": "approve-each"},
    "privacy": {"raw_customer_data": False, "examples": "synthetic"},
    "license": {"spdx": "Apache-2.0"},
    "provenance": {"approvals": "provenance/approvals.json"},
}

FLOW = {
    "flow": "0.1",
    "params": {"limit": 10},
    "inputs": {
        "olcum": {"type": "number", "prompt": "Ölçüm?", "unit": "bar", "min": 0, "max": 100},
        "acil": {"type": "bool", "prompt": "Acil mi?"},
    },
    "steps": [
        {"id": "a", "ask": "olcum"},
        {"id": "b", "compute": {"fark": "olcum - limit"}},
        {"id": "c", "decide": [
            {"when": "fark >= 0", "goto": "kayit"},
            {"else": True, "finish": "uygun"},
        ]},
        {"id": "kayit", "act": {"action": "record", "text": "Yüksek: {olcum}"}},
        {"id": "son", "finish": "yuksek"},
    ],
    "outcomes": {
        "uygun": {"verdict": "ok", "message": "Uygun: {olcum}"},
        "yuksek": {"verdict": "stop", "message": "Yüksek: {olcum}, fark {fark}"},
        "bilinmiyor": {"verdict": "escalate", "message": "Cevapsız: {missing}"},
    },
    "on_unknown": "bilinmiyor",
}

CASES = {
    "cases": [
        {"name": "alt", "inputs": {"olcum": 5}, "expect": {"outcome": "uygun"}},
        {"name": "üst", "inputs": {"olcum": 12}, "expect": {"outcome": "yuksek"}},
        {"name": "yok", "inputs": {}, "expect": {"outcome": "bilinmiyor"}},
    ],
    "routing": [{"utterance": "bir örnek ölçüm yapalım"}],
}


def write_pack(parent: Path, name: str = "ornek-paket", manifest=None, flow=None, cases=None) -> Path:
    manifest = copy.deepcopy(manifest or MANIFEST)
    manifest["name"] = name
    root = parent / name
    (root / "tests").mkdir(parents=True)
    (root / "provenance").mkdir()
    (root / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Example skill for tests.\n"
        'metadata:\n  skillpack-spec: "0.1-taslak"\n  skillpack-manifest: "skillpack.yaml"\n---\n# test\n',
        "utf-8",
    )
    (root / "skillpack.yaml").write_text(yaml.safe_dump(manifest, allow_unicode=True), "utf-8")
    (root / "flow.yaml").write_text(yaml.safe_dump(flow or FLOW, allow_unicode=True), "utf-8")
    (root / "tests" / "cases.yaml").write_text(yaml.safe_dump(cases or CASES, allow_unicode=True), "utf-8")
    (root / "provenance" / "approvals.json").write_text(
        json.dumps({"approvals": [{"approver": "t", "role": "usta", "date": "2026-11-10",
                                   "version": manifest["version"]}]}),
        "utf-8",
    )
    return root
