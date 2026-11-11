"""Akış yorumlayıcısı.

Paketteki adımları sırayla yürütür. Aynı girdi her zaman aynı sonucu verir:
burada model çağrısı yoktur, yalnız kural, tablo ve aritmetik vardır.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping

from . import expr
from .host import Host, Reading
from .pack import Pack

MAX_STEPS = 200
ASK_ATTEMPTS = 3

_TRUE = {"evet", "e", "yes", "y", "true", "1", "var"}
_FALSE = {"hayır", "hayir", "h", "no", "n", "false", "0", "yok"}
_PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")


class FlowError(Exception):
    """Akış yürütülemedi. Doğrulanmış bir pakette oluşmaması gerekir."""


@dataclass
class Result:
    skill: str
    version: str
    outcome: str
    verdict: str
    message: str
    values: dict[str, Any]
    trace: list[dict[str, Any]] = field(default_factory=list)
    suggested: list[dict[str, str]] = field(default_factory=list)
    performed: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill": self.skill,
            "version": self.version,
            "outcome": self.outcome,
            "verdict": self.verdict,
            "message": self.message,
            "values": self.values,
            "trace": self.trace,
            "suggested": self.suggested,
            "performed": self.performed,
        }


def coerce(spec: Mapping[str, Any], raw: Any) -> Any:
    """Ham cevabı girdinin türüne çevirir ve sınırlarını denetler."""
    kind = spec["type"]
    if kind == "bool":
        if isinstance(raw, bool):
            return raw
        text = str(raw).strip().lower()
        if text in _TRUE:
            return True
        if text in _FALSE:
            return False
        raise ValueError("evet ya da hayır bekleniyor")
    if kind == "choice":
        choices = spec["choices"]
        text = str(raw).strip().lower()
        if text in choices:
            return text
        if text.isdigit() and 1 <= int(text) <= len(choices):
            return choices[int(text) - 1]
        raise ValueError("seçeneklerden biri bekleniyor: " + ", ".join(choices))
    if isinstance(raw, bool):
        raise ValueError("sayı bekleniyor")
    if isinstance(raw, (int, float)):
        number = float(raw)
    else:
        try:
            number = float(str(raw).strip().replace(",", "."))
        except ValueError as exc:
            raise ValueError("sayı bekleniyor") from exc
    if number != number or number in (float("inf"), float("-inf")):
        raise ValueError("sayı bekleniyor")
    if kind == "integer":
        if number != int(number):
            raise ValueError("tam sayı bekleniyor")
        number = int(number)
    if "min" in spec and number < spec["min"]:
        raise ValueError(f"en az {fmt(spec['min'])} olmalı")
    if "max" in spec and number > spec["max"]:
        raise ValueError(f"en çok {fmt(spec['max'])} olmalı")
    return number


def fmt(value: Any) -> str:
    """Değeri kullanıcıya gösterilecek biçime çevirir."""
    if isinstance(value, bool):
        return "evet" if value else "hayır"
    if isinstance(value, float):
        text = f"{value:.2f}".rstrip("0").rstrip(".")
        return text.replace(".", ",")
    return str(value)


def render(template: str, env: Mapping[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in env:
            raise FlowError(f"yer tutucu doldurulamadı: {{{name}}}")
        return fmt(env[name])

    return _PLACEHOLDER.sub(replace, template)


def _lookup(table: Mapping[str, Any], key: Any) -> Any:
    if table["type"] == "map":
        rows = table["rows"]
        if key not in rows:
            raise FlowError(f"tabloda anahtar yok: {key}")
        return rows[key]
    if isinstance(key, bool) or not isinstance(key, (int, float)):
        raise FlowError("aralık tablosu sayısal anahtar ister")
    for row in table["rows"]:
        if "below" not in row or key < row["below"]:
            return row["value"]
    raise FlowError("aralık tablosunda eşleşme yok")


def run(
    pack: Pack,
    host: Host,
    prefilled: Mapping[str, Any] | None = None,
    prefilled_source: str = "kullanıcı",
) -> Result:
    """Paketin akışını yürütür.

    `prefilled`: yönlendiricinin konuşmadan çıkardığı değerler. Kaynak "model"
    ise her değer kullanılmadan önce insana doğrulatılır.
    """
    flow = pack.flow
    params = dict(flow.get("params") or {})
    inputs = flow["inputs"]
    tables = flow.get("tables") or {}
    steps = flow["steps"]
    outcomes = flow["outcomes"]
    index_of = {step["id"]: index for index, step in enumerate(steps)}
    prefilled = dict(prefilled or {})

    values: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []
    suggested: list[dict[str, str]] = []
    performed: list[dict[str, str]] = []

    def env() -> dict[str, Any]:
        return {**params, **values}

    def finish(outcome_id: str, extra: Mapping[str, Any] | None = None) -> Result:
        outcome = outcomes[outcome_id]
        message = render(outcome["message"], {**env(), **(extra or {})})
        trace.append({"kind": "finish", "outcome": outcome_id})
        return Result(
            skill=pack.name,
            version=pack.version,
            outcome=outcome_id,
            verdict=outcome["verdict"],
            message=message,
            values=dict(values),
            trace=trace,
            suggested=suggested,
            performed=performed,
        )

    def evaluate(source: str) -> Any:
        try:
            return expr.evaluate(source, env())
        except expr.ExprError as exc:
            raise FlowError(f"ifade değerlendirilemedi ({source}): {exc}") from exc

    def condition(source: str) -> bool:
        value = evaluate(source)
        if not isinstance(value, bool):
            raise FlowError(f"koşul mantıksal değer vermeli ({source})")
        return value

    sensor_cache: dict[str, Any] = {}

    def from_sensor(name: str) -> Any | None:
        """Sensör okuması; yoksa, geçersizse ya da bayatsa `None`. Okuma bir kez yapılır."""
        spec = inputs[name]
        if not spec.get("sensor"):
            return None
        if name in sensor_cache:
            return sensor_cache[name]
        sensor_cache[name] = None
        reading = host.read_sensor(spec["sensor"])
        if reading is None:
            return None
        if not isinstance(reading, Reading):
            reading = Reading(reading)
        limit = spec.get("max_age_s")
        if limit is not None and (reading.age_s is None or reading.age_s > limit):
            reason = "yaşı bilinmiyor" if reading.age_s is None else "bayat"
            entry = {"kind": "sensor", "name": name, "status": "reddedildi", "reason": reason}
            if reading.age_s is not None:
                entry["age_s"] = round(reading.age_s)
            trace.append(entry)
            return None
        try:
            sensor_cache[name] = coerce(spec, reading.value)
        except ValueError as exc:
            trace.append({"kind": "sensor", "name": name, "status": "reddedildi", "reason": str(exc)})
        return sensor_cache[name]

    def from_prefilled(name: str) -> Any | None:
        if name not in prefilled:
            return None
        try:
            return coerce(inputs[name], prefilled[name])
        except ValueError:
            return None

    def obtain(name: str) -> tuple[Any, str] | None:
        """Girdiyi sabit öncelikle edinir: sensör, konuşmadan çıkan değer, insan.

        Alttaki kaynak üsttekini ezemez: geçerli ve taze bir sensör okuması varken
        istemcinin ya da modelin verdiği değer kullanılmaz, yalnız ize yazılır.
        """
        spec = inputs[name]
        measured = from_sensor(name)
        given = from_prefilled(name)
        if measured is not None:
            if given is not None and given != measured:
                trace.append(
                    {"kind": "override", "name": name, "ignored": given,
                     "ignored_source": prefilled_source, "used": measured}
                )
            return measured, "sensör"
        if given is not None:
            if prefilled_source != "model":
                return given, prefilled_source
            unit = f" {spec['unit']}" if spec.get("unit") else ""
            if host.confirm(f"{spec['prompt']} → {fmt(given)}{unit}. Doğru mu?"):
                return given, "model+onay"
        for _ in range(ASK_ATTEMPTS):
            raw = host.ask(name, spec)
            if raw is None:
                return None
            try:
                return coerce(spec, raw), "insan"
            except ValueError as exc:
                host.say(f"Geçersiz cevap: {exc}.")
        return None

    hazards = flow.get("hazards") or []
    hazard_inputs = sorted(
        {name for hazard in hazards for name in expr.names(hazard["when"]) if name in inputs}
    )

    def hazard() -> Result | None:
        """Tehlike kurallarını o an bilinen değerlerle sınar.

        Sorulmamış girdiler için yalnız eldeki kaynaklara bakılır (sensör ve
        konuşmadan gelen değer); insana soru sorulmaz. Kural, bilinen değerlerle
        kesin doğruysa akış o sonuçla biter: eksik veri bilinen tehlikeyi örtmez.
        """
        if not hazards:
            return None
        known = env()
        passive: dict[str, tuple[Any, str]] = {}
        for name in hazard_inputs:
            if name in known:
                continue
            value = from_sensor(name)
            source = "sensör"
            if value is None:
                value, source = from_prefilled(name), prefilled_source
            if value is not None:
                passive[name] = (value, source)
                known[name] = value
        for index, rule in enumerate(hazards):
            try:
                fired = expr.evaluate(rule["when"], known, partial=True)
            except expr.ExprError as exc:
                raise FlowError(f"tehlike kuralı değerlendirilemedi ({rule['when']}): {exc}") from exc
            if fired is True:
                for name in sorted(expr.names(rule["when"]) & set(passive)):
                    values[name] = passive[name][0]
                    trace.append({"kind": "ask", "name": name, "value": passive[name][0],
                                  "source": passive[name][1], "step": "hazard"})
                trace.append({"kind": "hazard", "rule": index, "when": rule["when"],
                              "to": f"finish:{rule['finish']}"})
                return finish(rule["finish"])
        return None

    stopped = hazard()
    if stopped is not None:
        return stopped

    position = 0
    for _ in range(MAX_STEPS):
        if position >= len(steps):
            raise FlowError("akış bir sonuca varmadan bitti")
        step = steps[position]
        step_id = step["id"]
        position += 1

        if "ask" in step:
            name = step["ask"]
            if name in values:
                continue
            obtained = obtain(name)
            if obtained is None:
                trace.append({"step": step_id, "kind": "ask", "name": name, "value": None})
                return finish(flow["on_unknown"], {"missing": inputs[name]["prompt"]})
            values[name] = obtained[0]
            trace.append(
                {"step": step_id, "kind": "ask", "name": name, "value": obtained[0], "source": obtained[1]}
            )
            stopped = hazard()
            if stopped is not None:
                return stopped
        elif "compute" in step:
            assigned = {}
            for name, source in step["compute"].items():
                values[name] = assigned[name] = evaluate(source)
            trace.append({"step": step_id, "kind": "compute", "set": assigned})
            stopped = hazard()
            if stopped is not None:
                return stopped
        elif "lookup" in step:
            spec = step["lookup"]
            key = evaluate(spec["key"])
            values[spec["into"]] = _lookup(tables[spec["table"]], key)
            trace.append(
                {"step": step_id, "kind": "lookup", "table": spec["table"], "key": key, "value": values[spec["into"]]}
            )
            stopped = hazard()
            if stopped is not None:
                return stopped
        elif "decide" in step:
            for rule_index, rule in enumerate(step["decide"]):
                if "else" in rule or condition(rule["when"]):
                    entry = {"step": step_id, "kind": "decide", "rule": rule_index, "when": rule.get("when", "else")}
                    if "finish" in rule:
                        trace.append({**entry, "to": f"finish:{rule['finish']}"})
                        return finish(rule["finish"])
                    if "goto" in rule:
                        trace.append({**entry, "to": rule["goto"]})
                        position = index_of[rule["goto"]]
                    else:
                        trace.append({**entry, "to": "continue"})
                    break
        elif "say" in step:
            text = render(step["say"], env())
            host.say(text)
            trace.append({"step": step_id, "kind": "say", "text": text})
        elif "act" in step:
            action = step["act"]["action"]
            text = render(step["act"]["text"], env())
            record = {"action": action, "text": text}
            # İlke: kararı insan verir. `suggest` kipinde eylem hiç yapılmaz;
            # diğer kiplerde her eylem tek tek onaylatılır.
            if pack.mode != "suggest" and host.confirm(f"Eylem ({action}): {text} Onaylıyor musunuz?"):
                host.perform(action, text)
                performed.append(record)
                trace.append({"step": step_id, "kind": "act", **record, "status": "yapıldı"})
            else:
                suggested.append(record)
                trace.append({"step": step_id, "kind": "act", **record, "status": "önerildi"})
        elif "finish" in step:
            return finish(step["finish"])
        else:
            raise FlowError(f"adım tanınmadı: {step_id}")
    raise FlowError(f"akış {MAX_STEPS} adımı aştı (döngü olabilir)")
