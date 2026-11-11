"""`skillpack` komut satırı aracı."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from . import SPEC_VERSION, __version__
from .flow import FlowError, Result, coerce, fmt, run
from .host import ConsoleHost, ScriptedHost
from .pack import Pack, PackError, load_cases, validate_pack
from .registry import Registry
from .revocation import RevocationError, cached, publish, sync
from .router import KeywordRouter, OllamaRouter
from .signing import SigningError, generate_key, sign_pack, verify_pack
from .state import InstallState, StateError

VERDICT_LABEL = {"ok": "UYGUN", "warn": "DİKKAT", "stop": "DUR", "escalate": "USTAYA SOR"}


def _print_report(label: str, items: list[str]) -> None:
    for item in items:
        print(f"  {label}: {item}")


def _print_result(result: Result) -> None:
    print()
    print(f"[{VERDICT_LABEL[result.verdict]}] {result.message}")
    for action in result.suggested:
        print(f"  öneri ({action['action']}): {action['text']}")
    for action in result.performed:
        print(f"  yapıldı ({action['action']}): {action['text']}")
    print(f"  paket: {result.skill} {result.version} · sonuç: {result.outcome}")
    print("  gerekçe:")
    for entry in result.trace:
        kind = entry["kind"]
        if kind == "ask":
            value = "bilinmiyor" if entry["value"] is None else fmt(entry["value"])
            print(f"    {entry['name']} = {value} ({entry.get('source', '-')})")
        elif kind == "compute":
            for name, value in entry["set"].items():
                print(f"    {name} = {fmt(value)} (hesap)")
        elif kind == "lookup":
            print(f"    {entry['table']}[{fmt(entry['key'])}] = {fmt(entry['value'])} (tablo)")
        elif kind == "decide":
            print(f"    kural: {entry['when']} → {entry['to']}")


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.path)
    name = root.name
    if root.exists():
        print(f"hata: {root} zaten var", file=sys.stderr)
        return 1
    (root / "tests").mkdir(parents=True)
    (root / "provenance").mkdir()
    (root / "SKILL.md").write_text(
        f"""---
name: {name}
description: Describe in English what this skill checks and when to use it.
license: Apache-2.0
metadata:
  skillpack-spec: "{SPEC_VERSION}"
  skillpack-manifest: "skillpack.yaml"
---
# {name}

Bu paket bir akış (flow.yaml) taşır. Çalıştırıcı akışı yürütür; model yalnız
paketi seçer.
""",
        "utf-8",
    )
    (root / "skillpack.yaml").write_text(
        f"""skillpack: "{SPEC_VERSION}"
name: {name}
version: "0.1.0"
publisher: {{display: "Takma ad", org_role: bireysel}}
domain: {{sector: genel, task: {name}, lang: [tr]}}
components: {{procedure: SKILL.md, flow: flow.yaml, tests: tests/cases.yaml}}
runtime: {{llm_role: route-only}}
routing:
  title: "Paketin kısa Türkçe adı"
  triggers: ["anahtar sözcük"]
capabilities:
  tools: []
  network: none
  cloud_egress: {{allowed: false}}
human_in_loop: {{mode: suggest}}
privacy: {{raw_customer_data: false, examples: synthetic}}
license: {{spdx: Apache-2.0}}
provenance: {{approvals: provenance/approvals.json}}
""",
        "utf-8",
    )
    (root / "flow.yaml").write_text(
        """flow: "0.1"
params:
  limit: 10
inputs:
  olcum:
    type: number
    prompt: "Ölçüm değeri nedir?"
steps:
  - id: olcum_al
    ask: olcum
  - id: karar
    decide:
      - {when: "olcum >= limit", finish: yuksek}
      - {else: true, finish: uygun}
outcomes:
  uygun: {verdict: ok, message: "Ölçüm {olcum}, sınır {limit}. Uygun."}
  yuksek: {verdict: warn, message: "Ölçüm {olcum}, sınır {limit}. Yüksek."}
  bilinmiyor: {verdict: escalate, message: "Cevap alınamadı: {missing} Ustaya danışın."}
on_unknown: bilinmiyor
""",
        "utf-8",
    )
    (root / "tests" / "cases.yaml").write_text(
        """cases:
  - name: sınırın altı
    inputs: {olcum: 5}
    expect: {outcome: uygun}
  - name: sınırda
    inputs: {olcum: 10}
    expect: {outcome: yuksek}
  - name: cevap yok
    inputs: {}
    expect: {outcome: bilinmiyor}
routing:
  - utterance: "anahtar sözcük içeren örnek cümle"
""",
        "utf-8",
    )
    (root / "provenance" / "approvals.json").write_text(
        json.dumps(
            {
                "approvals": [
                    {
                        "approver": "Takma ad",
                        "role": "usta",
                        "date": "YYYY-AA-GG",
                        "version": "0.1.0",
                        "statement": "Kuralları okudum, benim yaptığım iş budur.",
                    }
                ]
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "utf-8",
    )
    print(f"iskelet oluşturuldu: {root}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    _, report = validate_pack(args.pack)
    _print_report("öneri", report.advice)
    _print_report("uyarı", report.warnings)
    _print_report("hata", report.errors)
    print("geçerli" if report.ok else "geçersiz")
    return 0 if report.ok else 1


def run_cases(pack: Pack) -> list[tuple[str, bool, str]]:
    results = []
    for case in load_cases(pack)["cases"]:
        host = ScriptedHost(
            answers=case.get("inputs") or {},
            sensors=case.get("sensors") or {},
            confirm=case.get("confirm", True),
        )
        expect = case["expect"]
        try:
            result = run(pack, host)
        except FlowError as exc:
            results.append((case["name"], False, f"akış hatası: {exc}"))
            continue
        problems = []
        if "outcome" in expect and result.outcome != expect["outcome"]:
            problems.append(f"sonuç {result.outcome}, beklenen {expect['outcome']}")
        if "verdict" in expect and result.verdict != expect["verdict"]:
            problems.append(f"hüküm {result.verdict}, beklenen {expect['verdict']}")
        for name, wanted in (expect.get("values") or {}).items():
            got = result.values.get(name)
            same = (
                abs(got - wanted) < 1e-9
                if isinstance(got, (int, float)) and isinstance(wanted, (int, float))
                and not isinstance(got, bool) and not isinstance(wanted, bool)
                else got == wanted
            )
            if not same:
                problems.append(f"{name} = {got}, beklenen {wanted}")
        results.append((case["name"], not problems, "; ".join(problems)))
    return results


def cmd_test(args: argparse.Namespace) -> int:
    pack, report = validate_pack(args.pack)
    if pack is None or not report.ok:
        _print_report("hata", report.errors)
        print("geçersiz paket; testler koşulmadı")
        return 1
    results = run_cases(pack)
    for name, passed, detail in results:
        print(f"  {'geçti' if passed else 'KALDI'}: {name}" + (f" — {detail}" if detail else ""))
    failed = sum(1 for _, passed, _ in results if not passed)
    print(f"{len(results) - failed}/{len(results)} vaka geçti")
    return 1 if failed else 0


def cmd_keygen(args: argparse.Namespace) -> int:
    identifier = generate_key(Path(args.out), Path(args.trust))
    print(f"özel anahtar: {args.out} (paylaşmayın, depoya koymayın)")
    print(f"açık anahtar: {Path(args.trust) / (identifier + '.pem')}")
    print(f"anahtar kimliği: {identifier}")
    return 0


def cmd_sign(args: argparse.Namespace) -> int:
    pack, report = validate_pack(args.pack)
    if pack is None or not report.ok:
        _print_report("hata", report.errors)
        print("geçersiz paket imzalanmaz")
        return 1
    failed = [name for name, passed, _ in run_cases(pack) if not passed]
    if failed:
        print("kabul testleri kaldı, paket imzalanmadı: " + ", ".join(failed))
        return 1
    bundle = sign_pack(Path(args.pack), Path(args.key))
    print(f"imzalandı: {bundle['name']} {bundle['version']}")
    print(f"paket kimliği: {bundle['pack_id']}")
    print(f"anahtar kimliği: {bundle['key_id']}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    revocations = Path(args.revocations) if args.revocations else None
    if args.revocation_cache:
        revocations = cached(Path(args.revocation_cache)).path
    result = verify_pack(Path(args.pack), Path(args.trust), revocations)
    _print_report("ret", result.reasons)
    if result.ok:
        print(f"doğrulandı: {result.pack_id} (anahtar {result.key_id})")
    return 0 if result.ok else 1


def _registry(args: argparse.Namespace) -> Registry:
    max_age = args.revocation_max_age_days
    return Registry(
        Path(args.packs),
        Path(args.trust),
        Path(args.revocations) if args.revocations else None,
        revocation_cache=Path(args.revocation_cache) if args.revocation_cache else None,
        revocation_max_age=None if max_age <= 0 else timedelta(days=max_age),
        state=InstallState(Path(args.state)) if args.state else None,
    )


def cmd_revocations_sync(args: argparse.Namespace) -> int:
    entry = sync(args.source, Path(args.root), Path(args.cache))
    count = len(json.loads(entry.path.read_text("utf-8"))["revoked"])
    print(f"iptal listesi doğrulandı ve eşitlendi: {count} kayıt")
    print(f"önbellek: {entry.path}")
    return 0


def cmd_revocations_status(args: argparse.Namespace) -> int:
    entry = cached(Path(args.cache))
    count = len(json.loads(entry.path.read_text("utf-8"))["revoked"])
    print(f"kayıt: {count}")
    print(f"kaynak: {entry.source}")
    print(f"son eşitleme: {entry.synced_at.isoformat(timespec='seconds')} "
          f"({entry.age().total_seconds() / 86400:.1f} gün önce)")
    return 0


def cmd_revocations_publish(args: argparse.Namespace) -> int:
    today = datetime.now(timezone.utc).date().isoformat()
    add = [{"pack_id": value, "reason": args.reason, "date": today} for value in args.pack_id or []]
    add += [{"key_id": value, "reason": args.reason, "date": today} for value in args.key_id or []]
    summary = publish(Path(args.repo), Path(args.keys), add, timestamp_days=args.timestamp_days)
    if summary["created"]:
        print(f"iptal deposu oluşturuldu: {args.repo}")
        print(f"istemcilere elden verilecek güven kökü: {summary['trusted_root']}")
        print(f"imza anahtarları: {args.keys} (paylaşmayın, depoya koymayın)")
    print(f"liste sürümü {summary['list_version']}, {summary['entries']} kayıt; "
          f"zaman damgası {summary['timestamp_expires']} tarihine kadar geçerli")
    return 0


def cmd_forget(args: argparse.Namespace) -> int:
    removed = InstallState(Path(args.state)).forget(args.name)
    print(f"kayıt silindi: {args.name}" if removed else f"kayıtta yok: {args.name}")
    return 0 if removed else 1


def cmd_list(args: argparse.Namespace) -> int:
    scan = _registry(args).scan()
    for name, pack in sorted(scan.packs.items()):
        print(f"{name} {pack.version} — {pack.title}")
    for rejected in scan.rejected:
        print(f"REDDEDİLDİ {rejected.path.name}: {'; '.join(rejected.reasons)}")
    if not scan.packs and not scan.rejected:
        print("paket bulunamadı")
    return 0


def _parse_sets(pack: Pack, pairs: list[str]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for pair in pairs:
        name, sep, raw = pair.partition("=")
        if not sep or name not in pack.flow["inputs"]:
            raise ValueError(f"geçersiz --set: {pair}")
        values[name] = coerce(pack.flow["inputs"][name], raw)
    return values


def _execute(
    pack: Pack, args: argparse.Namespace, prefilled: dict[str, Any], source: str
) -> int:
    host = ConsoleHost(journal=Path(args.journal) if args.journal else None)
    print(f"Paket: {pack.title} ({pack.name} {pack.version})")
    try:
        result = run(pack, host, prefilled=prefilled, prefilled_source=source)
    except FlowError as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        _print_result(result)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    scan = _registry(args).scan()
    pack = scan.packs.get(args.name)
    if pack is None:
        reasons = next((r.reasons for r in scan.rejected if r.path.name == args.name), None)
        detail = "; ".join(reasons) if reasons else "depoda yok"
        print(f"hata: {args.name} yüklenemedi: {detail}", file=sys.stderr)
        return 1
    try:
        prefilled = _parse_sets(pack, args.set or [])
    except ValueError as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 1
    return _execute(pack, args, prefilled, "kullanıcı")


def _router(args: argparse.Namespace):
    if args.router == "ollama":
        return OllamaRouter(model=args.model, url=args.ollama_url)
    return KeywordRouter()


def cmd_ask(args: argparse.Namespace) -> int:
    scan = _registry(args).scan()
    if not scan.packs:
        print("hata: yüklenebilen paket yok", file=sys.stderr)
        return 1
    route = _router(args).route(args.utterance, scan.packs)
    if route.note:
        print(f"not: {route.note}")
    if route.skill is None:
        print("Bu istek için paket seçilemedi. Yüklü paketler:")
        for name, pack in sorted(scan.packs.items()):
            print(f"  {name} — {pack.title}")
        return 2
    return _execute(scan.packs[route.skill], args, route.args, route.source)


def cmd_route_test(args: argparse.Namespace) -> int:
    scan = _registry(args).scan()
    router = _router(args)
    total = correct = 0
    for name, pack in sorted(scan.packs.items()):
        for example in load_cases(pack)["routing"]:
            total += 1
            route = router.route(example["utterance"], scan.packs)
            if route.skill == name:
                correct += 1
            else:
                print(f"  KALDI: \"{example['utterance']}\" → {route.skill}, beklenen {name}")
    print(f"{correct}/{total} yönlendirme doğru")
    return 0 if total and correct == total else 1


def cmd_serve(args: argparse.Namespace) -> int:
    from .mcp_server import Hub, serve_stdio

    sensors: dict[str, Path] = {}
    for pair in args.sensor or []:
        name, sep, path = pair.partition("=")
        if not sep or not name or not path:
            print(f"hata: geçersiz --sensor: {pair}", file=sys.stderr)
            return 1
        sensors[name] = Path(path)
    hub = Hub(_registry(args), sensors, Path(args.journal) if args.journal else None)
    try:
        serve_stdio(hub)
    except RuntimeError as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 1
    return 0


def _add_store(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--packs", default="examples", help="paket deposu dizini")
    parser.add_argument("--trust", default="examples/trust", help="güvenilen açık anahtarlar")
    parser.add_argument("--revocations", help="imzasız yerel iptal listesi (JSON); yalnız deneme için")
    parser.add_argument(
        "--revocation-cache", help="'revocations sync' ile doldurulan imzalı iptal önbelleği"
    )
    parser.add_argument(
        "--revocation-max-age-days", type=float, default=7,
        help="son eşitleme bundan eskiyse hiçbir paket yüklenmez (0 = sınır yok; varsayılan 7)",
    )
    parser.add_argument(
        "--state", help="kurulum kaydı (JSON): geri sarma ve yayıncı değişimine karşı koruma"
    )


def _add_router(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--router", choices=["keyword", "ollama"], default="keyword")
    parser.add_argument("--model", default="qwen2.5:7b", help="Ollama model adı")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillpack", description=f"skillpack {SPEC_VERSION} referans çalıştırıcısı"
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="yeni paket iskeleti")
    p.add_argument("path")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("validate", help="paketi standarda göre denetle")
    p.add_argument("pack")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("test", help="paketin kabul testlerini koş")
    p.add_argument("pack")
    p.set_defaults(func=cmd_test)

    p = sub.add_parser("keygen", help="Ed25519 anahtar çifti üret")
    p.add_argument("--out", required=True, help="özel anahtar dosyası")
    p.add_argument("--trust", required=True, help="açık anahtarın yazılacağı dizin")
    p.set_defaults(func=cmd_keygen)

    p = sub.add_parser("sign", help="doğrula, test et, imzala")
    p.add_argument("pack")
    p.add_argument("--key", required=True)
    p.set_defaults(func=cmd_sign)

    p = sub.add_parser("verify", help="imza, özet ve iptal denetimi")
    p.add_argument("pack")
    p.add_argument("--trust", default="examples/trust")
    p.add_argument("--revocations")
    p.add_argument("--revocation-cache")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("revocations", help="imzalı iptal listesi (TUF)")
    rsub = p.add_subparsers(dest="revocations_command", required=True)
    r = rsub.add_parser("sync", help="listeyi kaynaktan çek, doğrula, önbelleğe yaz")
    r.add_argument("--source", required=True, help="HTTP(S) adresi ya da yerel dizin (USB)")
    r.add_argument("--root", required=True, help="elden alınan güven kökü (1.root.json)")
    r.add_argument("--cache", required=True)
    r.set_defaults(func=cmd_revocations_sync)
    r = rsub.add_parser("status", help="önbellekteki listenin yaşı ve kayıt sayısı")
    r.add_argument("--cache", required=True)
    r.set_defaults(func=cmd_revocations_status)
    r = rsub.add_parser("publish", help="iptal deposunu oluştur, kayıt ekle ya da zaman damgasını tazele")
    r.add_argument("--repo", required=True, help="yayımlanacak dizin (metadata/ ve targets/)")
    r.add_argument("--keys", required=True, help="imza anahtarları dizini")
    r.add_argument("--pack-id", action="append", help="iptal edilecek paket kimliği (sha256:...)")
    r.add_argument("--key-id", action="append", help="iptal edilecek yayıncı anahtarı")
    r.add_argument(
        "--reason", default="guvenlik-acigi",
        choices=["zararli", "guvenlik-acigi", "lisans-ihlali", "yanlis-beyan", "yayinci-talebi"],
    )
    r.add_argument("--timestamp-days", type=float, default=7)
    r.set_defaults(func=cmd_revocations_publish)

    p = sub.add_parser("forget", help="bir paketi kurulum kaydından sil")
    p.add_argument("name")
    p.add_argument("--state", required=True)
    p.set_defaults(func=cmd_forget)

    p = sub.add_parser("list", help="depodaki paketleri listele")
    _add_store(p)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("run", help="adıyla bir paketi yürüt")
    p.add_argument("name")
    p.add_argument("--set", action="append", metavar="GİRDİ=DEĞER")
    p.add_argument("--journal", help="record eylemi için JSONL dosyası")
    p.add_argument("--json", action="store_true")
    _add_store(p)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("ask", help="serbest cümleyle iste; yönlendirici paketi seçer")
    p.add_argument("utterance")
    p.add_argument("--journal")
    p.add_argument("--json", action="store_true")
    _add_store(p)
    _add_router(p)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("serve", help="paketleri MCP araçları olarak sun (stdio)")
    p.add_argument("--journal", help="tamamlanan çalıştırmaların yazılacağı JSONL dosyası")
    p.add_argument(
        "--sensor", action="append", metavar="AD=DOSYA",
        help="sensör adını, güncel değeri içeren bir dosyaya bağla",
    )
    _add_store(p)
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("route-test", help="paketlerdeki yönlendirme örneklerini sına")
    _add_store(p)
    _add_router(p)
    p.set_defaults(func=cmd_route_test)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (PackError, SigningError, RevocationError, StateError) as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 1
