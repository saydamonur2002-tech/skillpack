"""MCP bağlaması: her paket, MCP üzerinden bir araç olarak sunulur.

Merkezde MCP konuşan herhangi bir istemci (yerel model çalıştıran bir uygulama)
durur; bu sunucu çevredeki dikey teknikleri ve onlara bağlı yazılımları ona açar.
Model aracı çağırır, karar yine pakettedir.

`Hub` MCP'den bağımsızdır ve tek başına sınanır. `serve_stdio`, resmî MCP Python
SDK'sını kullanarak Hub'ı stdio üzerinden yayınlar.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from . import __version__
from .flow import FlowError, coerce, fmt, run
from .host import Host
from .pack import Pack
from .registry import Registry

SERVER_INSTRUCTIONS = (
    "Each tool is a signed procedure written and approved by a human expert. "
    "The tool makes the decision; you do not. Pass only values the user stated "
    "explicitly. Omit everything else: the tool replies with the exact question "
    "to ask the user next. Pass null for a value the user says they do not know. "
    "Never guess or compute a value. Show the returned verdict message to the "
    "user unchanged."
)

_TOOL_RULE = (
    " The tool decides; do not decide yourself. Pass only values the user stated "
    "explicitly and omit the rest; the tool tells you what to ask next. Pass null "
    "when the user does not know. Show the verdict message to the user unchanged."
)


class _NeedInput(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name


class _HubHost(Host):
    """Akışın MCP üzerinden çalışırken gördüğü dünya.

    İnsana doğrudan soramaz: eksik girdide yürütmeyi keser, soru istemciye döner.
    Eylem onayı alamayacağı için hiçbir eylemi yapmaz; eylemler öneri olarak kalır.
    """

    def __init__(self, unknown: set[str], sensors: Mapping[str, Path]) -> None:
        self._unknown = unknown
        self._sensors = sensors

    def read_sensor(self, name: str) -> Any | None:
        path = self._sensors.get(name)
        if path is None:
            return None
        try:
            text = path.read_text("utf-8").strip()
        except OSError:
            return None
        return text or None

    def ask(self, name: str, spec: Mapping[str, Any]) -> Any | None:
        if name in self._unknown:
            return None
        raise _NeedInput(name)

    def confirm(self, text: str) -> bool:
        return False


@dataclass
class ToolOutcome:
    text: str
    structured: dict[str, Any]
    is_error: bool = False


def input_schema(pack: Pack) -> dict[str, Any]:
    """Paketin girdilerinden aracın JSON şemasını üretir. Her alan isteğe bağlıdır."""
    properties: dict[str, Any] = {}
    for name, spec in pack.flow["inputs"].items():
        description = spec["prompt"]
        if spec.get("unit"):
            description += f" ({spec['unit']})"
        if spec.get("hint"):
            description += f" — {spec['hint']}"
        description += " Null = user does not know."
        if spec["type"] in ("number", "integer"):
            prop: dict[str, Any] = {"type": [spec["type"], "null"]}
            if "min" in spec:
                prop["minimum"] = spec["min"]
            if "max" in spec:
                prop["maximum"] = spec["max"]
        elif spec["type"] == "bool":
            prop = {"type": ["boolean", "null"]}
        else:
            prop = {"type": ["string", "null"], "enum": [*spec["choices"], None]}
        prop["description"] = description
        properties[name] = prop
    return {"type": "object", "properties": properties, "additionalProperties": False}


def _question(name: str, spec: Mapping[str, Any]) -> dict[str, Any]:
    question = {"name": name, "prompt": spec["prompt"], "type": spec["type"]}
    for key in ("unit", "hint", "choices", "min", "max"):
        if key in spec:
            question[key] = spec[key]
    return question


def _question_text(question: Mapping[str, Any], reason: str | None = None) -> str:
    prompt = question["prompt"]
    if question.get("unit"):
        prompt += f" ({question['unit']})"
    if question.get("choices"):
        prompt += " [" + ", ".join(question["choices"]) + "]"
    lines = [f"INPUT REQUIRED: {question['name']}"]
    if reason:
        lines.append(f"The value given for \"{question['name']}\" was rejected: {reason}.")
    lines += [
        "Ask the user this question, then call the tool again with all previous "
        f"arguments plus \"{question['name']}\":",
        prompt,
    ]
    if question.get("hint"):
        lines.append(f"Hint for the user: {question['hint']}")
    lines.append("If the user does not know, pass null. Do not guess.")
    return "\n".join(lines)


_VERDICT = {"ok": "UYGUN", "warn": "DİKKAT", "stop": "DUR", "escalate": "USTAYA SOR"}


class Hub:
    """Depodaki paketleri araç olarak sunar ve çağrıları yürütür.

    Durumsuzdur: her çağrı akışı baştan, verilen değerlerle yürütür. Böylece aynı
    argümanlar her zaman aynı cevabı verir ve istemcide oturum tutmak gerekmez.
    """

    def __init__(
        self,
        registry: Registry,
        sensors: Mapping[str, Path] | None = None,
        journal: Path | None = None,
    ) -> None:
        self.registry = registry
        self.sensors = dict(sensors or {})
        self.journal = journal

    def tools(self) -> list[dict[str, Any]]:
        """Her listelemede depo yeniden taranır; yalnız imzası geçen paketler görünür."""
        return [
            {
                "name": name,
                "title": pack.title,
                "description": pack.description + _TOOL_RULE,
                "inputSchema": input_schema(pack),
            }
            for name, pack in sorted(self.registry.scan().packs.items())
        ]

    def call(self, name: str, arguments: Mapping[str, Any] | None) -> ToolOutcome:
        scan = self.registry.scan()
        pack = scan.packs.get(name)
        if pack is None:
            reasons = next((r.reasons for r in scan.rejected if r.path.name == name), None)
            detail = "; ".join(reasons) if reasons else "depoda yok"
            return self._error(f"Paket yüklenemedi ({name}): {detail}")

        inputs = pack.flow["inputs"]
        arguments = dict(arguments or {})
        unexpected = sorted(set(arguments) - set(inputs))
        if unexpected:
            return self._error(
                "Bilinmeyen argüman: " + ", ".join(unexpected)
                + ". Geçerli alanlar: " + ", ".join(inputs)
            )

        values: dict[str, Any] = {}
        unknown: set[str] = set()
        for key, raw in arguments.items():
            if raw is None:
                unknown.add(key)
                continue
            try:
                values[key] = coerce(inputs[key], raw)
            except ValueError as exc:
                question = _question(key, inputs[key])
                return ToolOutcome(
                    text=_question_text(question, reason=str(exc)),
                    structured={
                        "status": "needs_input",
                        "skill": pack.name,
                        "version": pack.version,
                        "ask": question,
                        "rejected": {"name": key, "reason": str(exc)},
                    },
                )

        try:
            result = run(
                pack,
                _HubHost(unknown, self.sensors),
                prefilled=values,
                prefilled_source="istemci",
            )
        except _NeedInput as need:
            question = _question(need.name, inputs[need.name])
            return ToolOutcome(
                text=_question_text(question),
                structured={
                    "status": "needs_input",
                    "skill": pack.name,
                    "version": pack.version,
                    "ask": question,
                },
            )
        except FlowError as exc:
            return self._error(f"Akış yürütülemedi: {exc}")

        structured = {"status": "done", **result.to_dict()}
        self._record(structured)
        lines = [f"[{_VERDICT[result.verdict]}] {result.message}"]
        for action in result.suggested:
            lines.append(f"Önerilen eylem (yapılmadı): {action['text']}")
        used = ", ".join(f"{key}={fmt(value)}" for key, value in result.values.items())
        lines.append(f"Kullanılan değerler: {used}")
        lines.append(f"Paket: {result.skill} {result.version} · sonuç: {result.outcome}")
        lines.append("Show the first line to the user unchanged.")
        return ToolOutcome(text="\n".join(lines), structured=structured)

    def _error(self, message: str) -> ToolOutcome:
        return ToolOutcome(text=message, structured={"status": "error", "message": message}, is_error=True)

    def _record(self, structured: Mapping[str, Any]) -> None:
        """Tamamlanan her çalıştırmayı kayıt defterine ekler (denetim izi)."""
        if self.journal is None:
            return
        entry = {
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "skill": structured["skill"],
            "version": structured["version"],
            "outcome": structured["outcome"],
            "verdict": structured["verdict"],
            "values": structured["values"],
        }
        with self.journal.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def build_server(hub: Hub):
    """Hub'ı resmî MCP SDK'sının sunucusuna bağlar."""
    try:
        from mcp import types
        from mcp.server.lowlevel import Server
    except ImportError as exc:  # pragma: no cover - kurulum ortamına bağlı
        raise RuntimeError(
            "MCP desteği için SDK gerekli: pip install 'skillpack[mcp]'"
        ) from exc

    async def list_tools(ctx, params) -> "types.ListToolsResult":
        return types.ListToolsResult(
            tools=[
                types.Tool(
                    name=tool["name"],
                    title=tool["title"],
                    description=tool["description"],
                    input_schema=tool["inputSchema"],
                )
                for tool in hub.tools()
            ]
        )

    async def call_tool(ctx, params) -> "types.CallToolResult":
        outcome = hub.call(params.name, params.arguments)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=outcome.text)],
            structured_content=outcome.structured,
            is_error=outcome.is_error,
        )

    return Server(
        "skillpack",
        version=__version__,
        title="skillpack",
        instructions=SERVER_INSTRUCTIONS,
        on_list_tools=list_tools,
        on_call_tool=call_tool,
    )


def serve_stdio(hub: Hub) -> None:
    """stdin/stdout üzerinden MCP sunar. stdout protokole aittir; oraya yazı yazılmaz."""
    import anyio
    from mcp.server.stdio import stdio_server

    server = build_server(hub)

    async def main() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    anyio.run(main)
