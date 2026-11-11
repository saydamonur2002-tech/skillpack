"""Yönlendirici: konuşmadan hangi paketin istendiğini seçer.

Dil modelinin tek görevi budur. Model karar vermez, hesap yapmaz, mesaj yazmaz;
yalnız (1) paketi seçer ve (2) kullanıcının açıkça söylediği değerleri çıkarır.
Çıkardığı her değer, kullanılmadan önce çalıştırıcı tarafından insana doğrulatılır.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Mapping

from .pack import Pack

_PUNCTUATION = re.compile(r"[^\w\s]", re.UNICODE)


@dataclass
class Route:
    skill: str | None
    args: dict[str, Any] = field(default_factory=dict)
    source: str = "anahtar-kelime"
    note: str | None = None


def normalize(text: str) -> str:
    """Türkçe büyük/küçük harf kurallarıyla küçültür, noktalamayı atar."""
    text = text.replace("İ", "i").replace("I", "ı").lower()
    return " ".join(_PUNCTUATION.sub(" ", text).split())


class KeywordRouter:
    """Modelsiz yönlendirici: paketin `routing.triggers` ifadelerini arar.

    Eşleşme alt dizge üzerindendir; böylece ek almış sözcükler de yakalanır
    ("rulman" → "rulmanı"). Eşitlik ya da sıfır puan durumunda seçim yapmaz.
    """

    def route(self, utterance: str, packs: Mapping[str, Pack]) -> Route:
        text = normalize(utterance)
        scores: dict[str, int] = {}
        for name, pack in packs.items():
            score = 0
            for trigger in pack.manifest["routing"]["triggers"]:
                phrase = normalize(trigger)
                if not phrase:
                    continue
                if phrase in text:
                    # longer phrases score higher; exact word boundary gets bonus
                    words = len(phrase.split())
                    score += words * 10
                    if f" {phrase} " in f" {text} ":
                        score += 5
            if score:
                scores[name] = score
        if not scores:
            return Route(skill=None, note="eşleşen paket yok")
        best = max(scores.values())
        winners = sorted(name for name, score in scores.items() if score == best)
        if len(winners) > 1:
            return Route(skill=None, note="birden çok paket eşit eşleşti: " + ", ".join(winners))
        return Route(skill=winners[0])


class OllamaRouter:
    """Yerel model (Ollama) ile yönlendirme.

    Çıktı JSON şemasıyla kısıtlanır: model yalnız var olan bir paket adını ya da
    "none" değerini üretebilir. Herhangi bir hata durumunda anahtar kelime
    yönlendiricisine düşülür.
    """

    def __init__(
        self,
        model: str,
        url: str = "http://127.0.0.1:11434",
        timeout: float = 60.0,
        fallback: KeywordRouter | None = None,
    ) -> None:
        self.model = model
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.fallback = fallback or KeywordRouter()
        self._opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def _chat(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(
            {
                "model": self.model,
                "stream": False,
                "format": schema,
                "options": {"temperature": 0},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with self._opener.open(request, timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = json.loads(payload["message"]["content"])
        if not isinstance(content, dict):
            raise ValueError("model bir JSON nesnesi döndürmedi")
        return content

    def route(self, utterance: str, packs: Mapping[str, Pack]) -> Route:
        if not packs:
            return Route(skill=None, source="model", note="yüklü paket yok")
        try:
            skill = self._select(utterance, packs)
            if skill is None:
                return Route(skill=None, source="model", note="model uygun paket bulmadı")
            args = self._extract(utterance, packs[skill])
            return Route(skill=skill, args=args, source="model")
        except (urllib.error.URLError, OSError, ValueError, KeyError) as exc:
            route = self.fallback.route(utterance, packs)
            route.note = f"model kullanılamadı ({exc}); anahtar kelimeyle yönlendirildi"
            return route

    def _select(self, utterance: str, packs: Mapping[str, Pack]) -> str | None:
        names = sorted(packs)
        choices = [{"name": name, "title": packs[name].title} for name in names]
        schema = {
            "type": "object",
            "properties": {
                "skill": {"type": "string", "enum": [*names, "none"]},
            },
            "required": ["skill"],
        }
        system = (
            "You are a router. Choose exactly one skill that matches the user's request. "
            "Return none if none fits. Do not invent a skill name."
        )
        user = json.dumps({"utterance": utterance, "skills": choices}, ensure_ascii=False)
        result = self._chat(system, user, schema)
        skill = result.get("skill")
        return skill if skill in packs else None

    def _extract(self, utterance: str, pack: Pack) -> dict[str, Any]:
        inputs = pack.flow["inputs"]
        properties = {}
        for name, spec in inputs.items():
            if spec["type"] in ("number", "integer"):
                prop: dict[str, Any] = {"type": [spec["type"], "null"]}
            elif spec["type"] == "bool":
                prop = {"type": ["boolean", "null"]}
            else:
                prop = {"type": ["string", "null"], "enum": [*spec["choices"], None]}
            properties[name] = prop
        schema = {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
        }
        system = (
            "Extract only values the user stated explicitly. "
            "Do not guess or compute. Use null for anything not stated."
        )
        user = json.dumps({"utterance": utterance, "inputs": list(inputs)}, ensure_ascii=False)
        content = self._chat(system, user, schema)
        # Şema modeli bağlasa da dönen JSON'a güvenilmez: boş ve tanımsız alanlar atılır.
        return {
            name: value
            for name, value in content.items()
            if name in properties and value is not None
        }
