"""Güvenli ifade değerlendirici.

Akış dosyasındaki `when`, `compute` ve `key` ifadeleri burada çalışır. Python'un
`eval` fonksiyonu kullanılmaz: ifade ayrıştırılır ve yalnız izin verilen düğümler
yorumlanır. Öznitelik erişimi, indeksleme, lambda ve serbest fonksiyon çağrısı yoktur.

Anlam kuralları spesifikasyon Bölüm 6.5'te tanımlıdır ve Python'un kendi
davranışından bağımsızdır: tür karışımı reddedilir, yuvarlama "yarım yukarı"dır,
sayılar sınırlıdır. Başka bir dilde yazılan çalıştırıcı aynı sonucu vermelidir.
"""

from __future__ import annotations

import ast
import math
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Mapping

MAX_LENGTH = 300
MAX_NODES = 100
MAX_ABS = 1e15
MAX_ROUND_DIGITS = 6

_BIN = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)
_ORDER = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)
_EQUAL = (ast.Eq, ast.NotEq)
_MEMBER = (ast.In, ast.NotIn)
_FUNCS = {"min", "max", "abs", "round"}
_LITERALS = {"true": True, "false": False}


class ExprError(Exception):
    """İfade geçersiz ya da değerlendirilemiyor."""


class _Unknown:
    """Değeri henüz bilinmeyen bir ada dayanan sonuç (üç değerli mantık)."""

    def __repr__(self) -> str:
        return "UNKNOWN"


UNKNOWN = _Unknown()


def _parse(source: str) -> ast.Expression:
    if not isinstance(source, str) or not source.strip():
        raise ExprError("boş ifade")
    if len(source) > MAX_LENGTH:
        raise ExprError(f"ifade {MAX_LENGTH} karakteri aşıyor")
    try:
        tree = ast.parse(source.strip(), mode="eval")
    except (SyntaxError, ValueError, RecursionError) as exc:
        raise ExprError(f"sözdizimi hatası: {getattr(exc, 'msg', exc)}") from exc
    if sum(1 for _ in ast.walk(tree)) > MAX_NODES:
        raise ExprError(f"ifade çok karmaşık ({MAX_NODES} düğümden fazla)")
    return tree


def _check(node: ast.AST) -> None:
    """İzin verilmeyen düğümü değerlendirmeden önce reddeder."""
    if isinstance(node, ast.Expression):
        _check(node.body)
    elif isinstance(node, ast.BoolOp):
        for value in node.values:
            _check(value)
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, (ast.Not, ast.USub)):
            raise ExprError("desteklenmeyen tekli işleç")
        _check(node.operand)
    elif isinstance(node, ast.BinOp):
        if not isinstance(node.op, _BIN):
            raise ExprError("desteklenmeyen işleç")
        _check(node.left)
        _check(node.right)
    elif isinstance(node, ast.Compare):
        _check(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, _MEMBER):
                if not isinstance(comparator, (ast.List, ast.Tuple)):
                    raise ExprError("in yalnız köşeli parantezli bir listeyle kullanılır")
                for element in comparator.elts:
                    literal = isinstance(element, ast.Name) and element.id in _LITERALS
                    if not literal and not isinstance(element, ast.Constant):
                        raise ExprError("in listesi yalnız sabit değer içerebilir")
                    _check(element)
            elif isinstance(op, _ORDER + _EQUAL):
                _check(comparator)
            else:
                raise ExprError("desteklenmeyen karşılaştırma")
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
            raise ExprError("yalnız min, max, abs, round çağrılabilir")
        if node.keywords:
            raise ExprError("adlı argüman desteklenmez")
        count = len(node.args)
        name = node.func.id
        if name in ("min", "max") and count < 2:
            raise ExprError(f"{name} en az iki argüman ister")
        if name == "abs" and count != 1:
            raise ExprError("abs tek argüman ister")
        if name == "round":
            if count not in (1, 2):
                raise ExprError("round bir ya da iki argüman ister")
            if count == 2:
                digits = node.args[1]
                if (
                    not isinstance(digits, ast.Constant)
                    or type(digits.value) is not int
                    or not 0 <= digits.value <= MAX_ROUND_DIGITS
                ):
                    raise ExprError(
                        f"round'un ikinci argümanı 0 ile {MAX_ROUND_DIGITS} arası sabit bir tam sayı olmalı"
                    )
        for arg in node.args:
            _check(arg)
    elif isinstance(node, (ast.List, ast.Tuple)):
        raise ExprError("liste yalnız in işlecinin sağında kullanılır")
    elif isinstance(node, ast.Constant):
        value = node.value
        if not isinstance(value, (int, float, str, bool)):
            raise ExprError("desteklenmeyen sabit")
        if _is_number(value) and not _in_range(value):
            raise ExprError("sabit sayı sınırın dışında")
    elif isinstance(node, ast.Name):
        pass
    else:
        raise ExprError(f"desteklenmeyen yapı: {type(node).__name__}")


def names(source: str) -> set[str]:
    """İfadenin başvurduğu değişken adları (fonksiyon ve true/false hariç)."""
    tree = _parse(source)
    _check(tree)
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in _LITERALS:
            found.add(node.id)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            found.discard(node.func.id)
    return found


def evaluate(source: str, env: Mapping[str, Any], partial: bool = False) -> Any:
    """İfadeyi değerlendirir.

    `partial` doğruysa ortamda bulunmayan ad hata değildir: sonuç ona bağlıysa
    `UNKNOWN` döner. `a or b` içinde `a` doğruysa `b` bilinmese de sonuç doğrudur.
    """
    tree = _parse(source)
    _check(tree)
    return _eval(tree.body, env, partial)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _in_range(value: Any) -> bool:
    return math.isfinite(value) and abs(value) <= MAX_ABS


def _kind(value: Any) -> str:
    if isinstance(value, bool):
        return "mantıksal"
    if isinstance(value, (int, float)):
        return "sayı"
    if isinstance(value, str):
        return "metin"
    return type(value).__name__


def _number(value: Any, what: str) -> Any:
    if not _is_number(value):
        raise ExprError(f"tür uyuşmazlığı: {what} sayı ister, {_kind(value)} verildi")
    return value


def _boolean(value: Any, what: str) -> bool:
    if not isinstance(value, bool):
        raise ExprError(f"tür uyuşmazlığı: {what} mantıksal değer ister, {_kind(value)} verildi")
    return value


def _result(value: Any) -> Any:
    if not _in_range(value):
        raise ExprError("sonuç sayı sınırının dışında")
    return value


def _same_kind(left: Any, right: Any) -> None:
    if _kind(left) != _kind(right):
        raise ExprError(
            f"tür uyuşmazlığı: {_kind(left)} ile {_kind(right)} karşılaştırılamaz"
        )


def _round(value: Any, digits: int | None) -> Any:
    """Yarım yukarı (sıfırdan uzağa) yuvarlar: 2,5 → 3; -2,5 → -3."""
    quantum = Decimal(1) if not digits else Decimal(1).scaleb(-digits)
    rounded = Decimal(repr(value)).quantize(quantum, rounding=ROUND_HALF_UP)
    return int(rounded) if not digits else float(rounded)


def _eval(node: ast.AST, env: Mapping[str, Any], partial: bool) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in _LITERALS:
            return _LITERALS[node.id]
        if node.id not in env:
            if partial:
                return UNKNOWN
            raise ExprError(f"tanımsız değişken: {node.id}")
        value = env[node.id]
        if not isinstance(value, (int, float, str, bool)):
            raise ExprError(f"desteklenmeyen değer türü: {node.id}")
        return value
    if isinstance(node, ast.BoolOp):
        # Kleene mantığı: belirleyici bir işlenen varsa bilinmeyen sonucu etkilemez.
        decisive = isinstance(node.op, ast.Or)
        unknown = False
        for operand in node.values:
            value = _eval(operand, env, partial)
            if value is UNKNOWN:
                unknown = True
                continue
            if _boolean(value, "and/or") is decisive:
                return decisive
        return UNKNOWN if unknown else not decisive
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, env, partial)
        if operand is UNKNOWN:
            return UNKNOWN
        if isinstance(node.op, ast.Not):
            return not _boolean(operand, "not")
        return -_number(operand, "eksi işareti")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left, env, partial)
        right = _eval(node.right, env, partial)
        if left is UNKNOWN or right is UNKNOWN:
            return UNKNOWN
        _number(left, "aritmetik")
        _number(right, "aritmetik")
        if isinstance(node.op, ast.Add):
            return _result(left + right)
        if isinstance(node.op, ast.Sub):
            return _result(left - right)
        if isinstance(node.op, ast.Mult):
            return _result(left * right)
        if right == 0:
            raise ExprError("sıfıra bölme")
        if isinstance(node.op, ast.Div):
            return _result(left / right)
        return _result(left % right)
    if isinstance(node, ast.Compare):
        left = _eval(node.left, env, partial)
        unknown = left is UNKNOWN
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, _MEMBER):
                if unknown:
                    return UNKNOWN
                items = [_eval(element, env, partial) for element in comparator.elts]
                found = any(_kind(left) == _kind(item) and left == item for item in items)
                return found if isinstance(op, ast.In) else not found
            right = _eval(comparator, env, partial)
            if right is UNKNOWN or unknown:
                unknown = True
                left = right
                continue
            if isinstance(op, _EQUAL):
                _same_kind(left, right)
                holds = (left == right) if isinstance(op, ast.Eq) else (left != right)
            else:
                _number(left, "sıralama")
                _number(right, "sıralama")
                holds = (
                    left < right if isinstance(op, ast.Lt)
                    else left <= right if isinstance(op, ast.LtE)
                    else left > right if isinstance(op, ast.Gt)
                    else left >= right
                )
            if not holds:
                return False
            left = right
        return UNKNOWN if unknown else True
    if isinstance(node, ast.Call):
        args = [_eval(arg, env, partial) for arg in node.args]
        if any(arg is UNKNOWN for arg in args):
            return UNKNOWN
        name = node.func.id
        if name == "round":
            return _result(_round(_number(args[0], "round"), args[1] if len(args) == 2 else None))
        for arg in args:
            _number(arg, name)
        if name == "abs":
            return _result(abs(args[0]))
        return min(args) if name == "min" else max(args)
    raise ExprError(f"desteklenmeyen yapı: {type(node).__name__}")
