"""Paketi diskten okur ve standarda uygunluğunu denetler."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from . import SPEC_VERSION, expr

MANIFEST_FILE = "skillpack.yaml"
SKILL_FILE = "SKILL.md"
SIGNATURE_FILE = "skillpack.sig.json"

# Çalıştırıcının sağladığı eylem ilkelleri. Paket bunların dışında eylem isteyemez.
HOST_ACTIONS = {"notify", "record"}
RESERVED_NAMES = {"missing", "true", "false", "min", "max", "abs", "round"}

_PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")
_STEP_KINDS = ("ask", "compute", "lookup", "decide", "say", "act", "finish")


class PackError(Exception):
    """Paket okunamıyor."""


@dataclass
class Pack:
    path: Path
    manifest: dict[str, Any]
    flow: dict[str, Any]
    skill: dict[str, Any]

    @property
    def name(self) -> str:
        return self.manifest["name"]

    @property
    def version(self) -> str:
        return self.manifest["version"]

    @property
    def title(self) -> str:
        return self.manifest["routing"]["title"]

    @property
    def description(self) -> str:
        return str(self.skill.get("description", "")).strip()

    @property
    def mode(self) -> str:
        return self.manifest["human_in_loop"]["mode"]


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_schema(name: str) -> dict[str, Any]:
    text = resources.files("skillpack").joinpath("schemas", name).read_text("utf-8")
    return json.loads(text)


def _read_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text("utf-8"))
    except FileNotFoundError as exc:
        raise PackError(f"dosya yok: {path.name}") from exc
    except yaml.YAMLError as exc:
        raise PackError(f"{path.name} YAML olarak okunamadı: {exc}") from exc


def read_frontmatter(path: Path) -> dict[str, Any]:
    """SKILL.md başındaki `---` arası YAML ön bilgisini döndürür."""
    try:
        text = path.read_text("utf-8")
    except FileNotFoundError as exc:
        raise PackError(f"dosya yok: {path.name}") from exc
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise PackError(f"{path.name} ön bilgi (---) ile başlamıyor")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise PackError(f"{path.name} ön bilgisi kapanmıyor") from exc
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise PackError(f"{path.name} ön bilgisi okunamadı: {exc}") from exc
    if not isinstance(data, dict):
        raise PackError(f"{path.name} ön bilgisi bir eşleme olmalı")
    return data


def _inside(root: Path, relative: str) -> Path:
    """Paket içi yolu çözer; paket dışına çıkan yolu reddeder."""
    target = (root / relative).resolve()
    if root.resolve() not in target.parents and target != root.resolve():
        raise PackError(f"yol paket dışına çıkıyor: {relative}")
    return target


def load_pack(path: Path | str) -> Pack:
    root = Path(path)
    if not root.is_dir():
        raise PackError(f"paket dizini yok: {root}")
    manifest = _read_yaml(root / MANIFEST_FILE)
    if not isinstance(manifest, dict):
        raise PackError(f"{MANIFEST_FILE} bir eşleme olmalı")
    flow_ref = (manifest.get("components") or {}).get("flow")
    if not isinstance(flow_ref, str):
        raise PackError("components.flow tanımlı değil")
    flow = _read_yaml(_inside(root, flow_ref))
    if not isinstance(flow, dict):
        raise PackError(f"{flow_ref} bir eşleme olmalı")
    skill = read_frontmatter(root / SKILL_FILE)
    return Pack(path=root, manifest=manifest, flow=flow, skill=skill)


def _schema_errors(schema_name: str, data: Any, label: str) -> list[str]:
    validator = Draft202012Validator(load_schema(schema_name))
    found = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(part) for part in error.path) or "(kök)"
        found.append(f"{label}: {where}: {error.message}")
    return found


def placeholders(template: str) -> set[str]:
    return set(_PLACEHOLDER.findall(template))


def check_flow(flow: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    """Şemanın yakalayamadığı anlamsal kuralları denetler."""
    errors: list[str] = []
    params = flow.get("params") or {}
    inputs = flow["inputs"]
    tables = flow.get("tables") or {}
    steps = flow["steps"]
    outcomes = flow["outcomes"]

    for name, spec in inputs.items():
        if spec["type"] == "choice" and not spec.get("choices"):
            errors.append(f"girdi {name}: choice türü için choices gerekli")
        if spec["type"] != "choice" and "choices" in spec:
            errors.append(f"girdi {name}: choices yalnız choice türünde kullanılır")
        if "min" in spec and "max" in spec and spec["min"] > spec["max"]:
            errors.append(f"girdi {name}: min, max değerinden büyük")
    declared_sensors = set((manifest.get("capabilities") or {}).get("sensors") or [])
    for name, spec in inputs.items():
        if "sensor" in spec and spec["sensor"] not in declared_sensors:
            errors.append(
                f"girdi {name}: sensör '{spec['sensor']}' capabilities.sensors içinde beyan edilmemiş"
            )

    for name, table in tables.items():
        if table["type"] == "range":
            rows = table["rows"]
            bounds = [row.get("below") for row in rows[:-1]]
            if any(bound is None for bound in bounds) or "below" in rows[-1]:
                errors.append(
                    f"tablo {name}: son satır dışındaki her satırda below olmalı, son satırda olmamalı"
                )
            elif bounds != sorted(bounds):
                errors.append(f"tablo {name}: below değerleri artan sırada olmalı")

    # Ad uzayı: parametre, girdi ve hesaplanan değerler tek uzayı paylaşır.
    computed: set[str] = set()
    for step in steps:
        computed.update((step.get("compute") or {}).keys())
        if "lookup" in step:
            computed.add(step["lookup"]["into"])
    known = set(params) | set(inputs) | computed
    for group, label in ((params, "parametre"), (inputs, "girdi"), (computed, "değişken")):
        for name in group:
            if name in RESERVED_NAMES:
                errors.append(f"{label} adı ayrılmış: {name}")
    for name in set(params) & set(inputs):
        errors.append(f"ad hem parametre hem girdi: {name}")
    for name in computed & (set(params) | set(inputs)):
        errors.append(f"hesaplanan değer bir parametre ya da girdiyi eziyor: {name}")

    def check_expr(source: str, where: str) -> None:
        try:
            unknown = expr.names(source) - known
        except expr.ExprError as exc:
            errors.append(f"{where}: {exc}")
            return
        for name in sorted(unknown):
            errors.append(f"{where}: tanımsız ad '{name}'")

    def check_template(template: str, where: str, extra: set[str] = frozenset()) -> None:
        for name in sorted(placeholders(template) - known - extra):
            errors.append(f"{where}: tanımsız yer tutucu '{{{name}}}'")

    ids = [step["id"] for step in steps]
    for step_id in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"adım kimliği yinelenmiş: {step_id}")
    id_set = set(ids)

    declared_tools = set((manifest.get("capabilities") or {}).get("tools") or [])
    for tool in sorted(declared_tools):
        if tool.removeprefix("host:") not in HOST_ACTIONS:
            errors.append(f"capabilities.tools: bilinmeyen araç '{tool}'")

    for step in steps:
        where = f"adım {step['id']}"
        kinds = [kind for kind in _STEP_KINDS if kind in step]
        if len(kinds) != 1:
            errors.append(f"{where}: tam olarak bir işlem içermeli ({', '.join(_STEP_KINDS)})")
            continue
        kind = kinds[0]
        if kind == "ask":
            if step["ask"] not in inputs:
                errors.append(f"{where}: tanımsız girdi '{step['ask']}'")
        elif kind == "compute":
            for name, source in step["compute"].items():
                check_expr(source, f"{where}.compute.{name}")
        elif kind == "lookup":
            if step["lookup"]["table"] not in tables:
                errors.append(f"{where}: tanımsız tablo '{step['lookup']['table']}'")
            check_expr(step["lookup"]["key"], f"{where}.lookup.key")
        elif kind == "decide":
            rules = step["decide"]
            for index, rule in enumerate(rules):
                rule_where = f"{where}.decide[{index}]"
                if ("when" in rule) == ("else" in rule):
                    errors.append(f"{rule_where}: when ya da else'ten tam biri olmalı")
                targets = [key for key in ("goto", "finish", "continue") if key in rule]
                if len(targets) != 1:
                    errors.append(f"{rule_where}: goto, finish, continue'dan tam biri olmalı")
                if "when" in rule:
                    check_expr(rule["when"], rule_where)
                if "goto" in rule and rule["goto"] not in id_set:
                    errors.append(f"{rule_where}: tanımsız adım '{rule['goto']}'")
                if "finish" in rule and rule["finish"] not in outcomes:
                    errors.append(f"{rule_where}: tanımsız sonuç '{rule['finish']}'")
                if "else" in rule and index != len(rules) - 1:
                    errors.append(f"{rule_where}: else yalnız son kural olabilir")
            if "else" not in rules[-1]:
                errors.append(f"{where}: son kural else olmalı (kapsanmayan durum kalamaz)")
        elif kind == "say":
            check_template(step["say"], where)
        elif kind == "act":
            action = step["act"]["action"]
            if f"host:{action}" not in declared_tools:
                errors.append(
                    f"{where}: eylem '{action}' capabilities.tools içinde beyan edilmemiş"
                )
            check_template(step["act"]["text"], where)
        elif kind == "finish":
            if step["finish"] not in outcomes:
                errors.append(f"{where}: tanımsız sonuç '{step['finish']}'")

    last = steps[-1]
    falls_off = "finish" not in last and not (
        "decide" in last and all("continue" not in rule for rule in last["decide"])
    )
    if falls_off:
        errors.append("son adım finish olmalı ya da tüm dalları goto/finish ile biten bir decide olmalı")

    for name, outcome in outcomes.items():
        check_template(outcome["message"], f"sonuç {name}", extra={"missing"})
    if flow["on_unknown"] not in outcomes:
        errors.append(f"on_unknown tanımsız sonuca işaret ediyor: {flow['on_unknown']}")
    elif outcomes[flow["on_unknown"]]["verdict"] != "escalate":
        errors.append("on_unknown sonucunun verdict değeri escalate olmalı")
    return errors


_PII = {
    "e-posta": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "telefon": re.compile(r"(?:\+90|0)[\s-]*5\d{2}(?:[\s-]*\d){7}"),
    "IBAN": re.compile(r"TR(?:\s*\d){24}", re.IGNORECASE),
    "11 haneli numara": re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)"),
}
_TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}


def scan_pii(root: Path) -> list[str]:
    """Kişisel veri kalıbı arar. Yardımcıdır, garanti değildir."""
    found = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in _TEXT_SUFFIXES:
            continue
        if path.name == SIGNATURE_FILE:
            continue
        text = path.read_text("utf-8", errors="replace")
        for label, pattern in _PII.items():
            if pattern.search(text):
                found.append(f"{path.relative_to(root).as_posix()}: olası {label}")
    return found


def validate_pack(path: Path | str) -> tuple[Pack | None, Report]:
    report = Report()
    try:
        pack = load_pack(path)
    except PackError as exc:
        report.errors.append(str(exc))
        return None, report

    report.errors += _schema_errors("skillpack.schema.json", pack.manifest, MANIFEST_FILE)
    flow_ref = pack.manifest["components"]["flow"]
    report.errors += _schema_errors("flow.schema.json", pack.flow, flow_ref)
    if report.errors:
        return pack, report

    known_fields = set(load_schema("skillpack.schema.json")["properties"])
    for key in sorted(set(pack.manifest) - known_fields):
        report.warnings.append(f"{MANIFEST_FILE}: bilinmeyen alan yok sayıldı: {key}")

    manifest = pack.manifest
    if pack.path.resolve().name != manifest["name"]:
        report.errors.append(
            f"dizin adı ({pack.path.resolve().name}) ile name ({manifest['name']}) aynı olmalı"
        )
    if pack.skill.get("name") != manifest["name"]:
        report.errors.append(f"{SKILL_FILE} name alanı manifestteki name ile aynı olmalı")
    if not pack.description:
        report.errors.append(f"{SKILL_FILE} description alanı boş")
    metadata = pack.skill.get("metadata") or {}
    if metadata.get("skillpack-spec") != SPEC_VERSION:
        report.errors.append(f"{SKILL_FILE} metadata.skillpack-spec '{SPEC_VERSION}' olmalı")
    if metadata.get("skillpack-manifest") != MANIFEST_FILE:
        report.errors.append(f"{SKILL_FILE} metadata.skillpack-manifest '{MANIFEST_FILE}' olmalı")

    capabilities = manifest["capabilities"]
    if capabilities["network"] != "none":
        report.errors.append("capabilities.network: bu çalıştırıcı yalnız 'none' destekler")
    if capabilities["cloud_egress"]["allowed"]:
        report.errors.append("capabilities.cloud_egress.allowed: bu çalıştırıcı yalnız false destekler")

    report.errors += check_flow(pack.flow, manifest)

    try:
        approvals_path = _inside(pack.path, manifest["provenance"]["approvals"])
        approvals = json.loads(approvals_path.read_text("utf-8"))
    except (PackError, OSError, json.JSONDecodeError) as exc:
        report.errors.append(f"onay kaydı okunamadı: {exc}")
    else:
        entries = approvals.get("approvals") if isinstance(approvals, dict) else None
        if not entries:
            report.errors.append("onay kaydında en az bir insan onayı olmalı")
        else:
            for index, entry in enumerate(entries):
                for key in ("approver", "role", "date", "version"):
                    if not isinstance(entry, dict) or not entry.get(key):
                        report.errors.append(f"onay kaydı [{index}]: {key} eksik")
            if not any(
                isinstance(entry, dict) and entry.get("version") == manifest["version"]
                for entry in entries
            ):
                report.errors.append(f"onay kaydında {manifest['version']} sürümü için onay yok")

    try:
        cases = load_cases(pack)
    except PackError as exc:
        report.errors.append(str(exc))
    else:
        if not cases["cases"]:
            report.errors.append("kabul testi yok: en az bir vaka gerekli")
        reached = {case.get("expect", {}).get("outcome") for case in cases["cases"]}
        for name in sorted(set(pack.flow["outcomes"]) - reached):
            report.warnings.append(f"hiçbir kabul testi '{name}' sonucunu sınamıyor")
        if not cases["routing"]:
            report.warnings.append("yönlendirme örneği yok (routing)")

    for hit in scan_pii(pack.path):
        report.warnings.append(f"kişisel veri taraması: {hit}")
    return pack, report


def load_cases(pack: Pack) -> dict[str, list[dict[str, Any]]]:
    path = _inside(pack.path, pack.manifest["components"]["tests"])
    data = _read_yaml(path)
    if not isinstance(data, dict):
        raise PackError(f"{path.name} bir eşleme olmalı")
    cases = data.get("cases") or []
    routing = data.get("routing") or []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or "name" not in case or "expect" not in case:
            raise PackError(f"{path.name}: cases[{index}] name ve expect içermeli")
    for index, example in enumerate(routing):
        if not isinstance(example, dict) or not isinstance(example.get("utterance"), str):
            raise PackError(f"{path.name}: routing[{index}] utterance içermeli")
    return {"cases": cases, "routing": routing}
