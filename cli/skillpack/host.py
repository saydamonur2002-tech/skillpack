"""Çalıştırıcının dış dünyayla tek temas noktası.

Akış yalnız bu arayüz üzerinden insana soru sorar, sensör okur ve eylem yapar.
Yeni bir ortam (telefon, Home Assistant, PLC) eklemek bu sınıfı uyarlamak demektir.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

UNKNOWN_WORDS = {"", "?", "bilmiyorum", "bilmem", "emin değilim"}


class Host:
    """Varsayılan davranış: sensör yok, her soru bilinmiyor, eylem yapılmaz."""

    def read_sensor(self, name: str) -> Any | None:
        return None

    def ask(self, name: str, spec: Mapping[str, Any]) -> Any | None:
        """Ham cevabı döndürür. `None` = insan bilmiyor."""
        return None

    def confirm(self, text: str) -> bool:
        return False

    def say(self, text: str) -> None:
        pass

    def perform(self, action: str, text: str) -> None:
        raise NotImplementedError(action)


class ConsoleHost(Host):
    """Terminalde insanla konuşur."""

    def __init__(
        self,
        sensors: Mapping[str, Callable[[], Any]] | None = None,
        journal: Path | None = None,
        stdin=None,
        stdout=None,
    ) -> None:
        self._sensors = dict(sensors or {})
        self._journal = journal
        self._in = stdin or sys.stdin
        self._out = stdout or sys.stdout

    def _print(self, text: str) -> None:
        print(text, file=self._out, flush=True)

    def _readline(self) -> str | None:
        line = self._in.readline()
        if line == "":
            return None
        return line.strip()

    def read_sensor(self, name: str) -> Any | None:
        reader = self._sensors.get(name)
        return reader() if reader else None

    def ask(self, name: str, spec: Mapping[str, Any]) -> Any | None:
        prompt = spec["prompt"]
        if spec.get("unit"):
            prompt += f" ({spec['unit']})"
        if spec["type"] == "bool":
            prompt += " [evet/hayır]"
        if spec["type"] == "choice":
            options = ", ".join(
                f"{i}) {choice}" for i, choice in enumerate(spec["choices"], 1)
            )
            prompt += f" [{options}]"
        self._print(f"? {prompt}")
        if spec.get("hint"):
            self._print(f"  ({spec['hint']})")
        answer = self._readline()
        if answer is None or answer.lower() in UNKNOWN_WORDS:
            return None
        return answer

    def confirm(self, text: str) -> bool:
        self._print(f"? {text} [evet/hayır]")
        answer = self._readline()
        return answer is not None and answer.lower() in {"evet", "e", "yes", "y"}

    def say(self, text: str) -> None:
        self._print(f"  {text}")

    def perform(self, action: str, text: str) -> None:
        if action == "notify":
            self._print(f"[bildirim] {text}")
        elif action == "record":
            if self._journal is None:
                self._print(f"[kayıt] {text}")
            else:
                entry = {
                    "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "text": text,
                }
                with self._journal.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
                self._print(f"[kayıt] {self._journal} dosyasına yazıldı")
        else:
            raise NotImplementedError(action)


class ScriptedHost(Host):
    """Testler için: cevaplar baştan verilir, yapılanlar kaydedilir."""

    def __init__(
        self,
        answers: Mapping[str, Any] | None = None,
        sensors: Mapping[str, Any] | None = None,
        confirm: bool = True,
    ) -> None:
        self.answers = dict(answers or {})
        self.sensors = dict(sensors or {})
        self.confirm_answer = confirm
        self.asked: list[str] = []
        self.said: list[str] = []
        self.confirmed: list[str] = []
        self.performed: list[tuple[str, str]] = []

    def read_sensor(self, name: str) -> Any | None:
        return self.sensors.get(name)

    def ask(self, name: str, spec: Mapping[str, Any]) -> Any | None:
        self.asked.append(name)
        return self.answers.get(name)

    def confirm(self, text: str) -> bool:
        self.confirmed.append(text)
        return self.confirm_answer

    def say(self, text: str) -> None:
        self.said.append(text)

    def perform(self, action: str, text: str) -> None:
        self.performed.append((action, text))
