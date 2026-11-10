"""Güvenli ifade değerlendirici.

Akış dosyasındaki `when`, `compute` ve `key` ifadeleri burada çalışır. Python'un
`eval` fonksiyonu kullanılmaz: ifade ayrıştırılır ve yalnız izin verilen düğümler
yorumlanır. Öznitelik erişimi, indeksleme, lambda ve serbest fonksiyon çağrısı yoktur.
"""

from __future__ import annotations

import ast
import operator
from typing import Any, Mapping

MAX_LENGTH = 300

_BIN = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
}
_CMP = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
}
_FUNCS = {"min": min, "max": max, "abs": abs, "round": round}
_LITERALS = {"true": True, "false": False}


class ExprError(Exception):
    """İfade geçersiz ya da değerlendirilemiyor."""


def _parse(source: str) -> ast.Expression:
    if not isinstance(source, str) or not source.strip():
        raise ExprError("boş ifade")
    if len(source) > MAX_LENGTH:
        raise ExprError(f"ifade {MAX_LENGTH} karakteri aşıyor")
    try:
        return ast.parse(source.strip(), mode="eval")
    except SyntaxError as exc:
        raise ExprError(f"sözdizimi hatası: {exc.msg}") from exc


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
        if type(node.op) not in _BIN:
            raise ExprError("desteklenmeyen işleç")
        _check(node.left)
        _check(node.right)
    elif isinstance(node, ast.Compare):
        for op in node.ops:
            if type(op) not in _CMP:
                raise ExprError("desteklenmeyen karşılaştırma")
        _check(node.left)
        for comparator in node.comparators:
            _check(comparator)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
            raise ExprError("yalnız min, max, abs, round çağrılabilir")
        if node.keywords:
            raise ExprError("adlı argüman desteklenmez")
        for arg in node.args:
            _check(arg)
    elif isinstance(node, (ast.List, ast.Tuple)):
        for element in node.elts:
            _check(element)
    elif isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float, str, bool)):
            raise ExprError("desteklenmeyen sabit")
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


def evaluate(source: str, env: Mapping[str, Any]) -> Any:
    tree = _parse(source)
    _check(tree)
    try:
        return _eval(tree.body, env)
    except ExprError:
        raise
    except ZeroDivisionError as exc:
        raise ExprError("sıfıra bölme") from exc
    except TypeError as exc:
        raise ExprError(f"tür uyuşmazlığı: {exc}") from exc


def _eval(node: ast.AST, env: Mapping[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in _LITERALS:
            return _LITERALS[node.id]
        if node.id not in env:
            raise ExprError(f"tanımsız değişken: {node.id}")
        return env[node.id]
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(_eval(value, env) for value in node.values)
        return any(_eval(value, env) for value in node.values)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, env)
        return (not operand) if isinstance(node.op, ast.Not) else -operand
    if isinstance(node, ast.BinOp):
        return _BIN[type(node.op)](_eval(node.left, env), _eval(node.right, env))
    if isinstance(node, ast.Compare):
        left = _eval(node.left, env)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator, env)
            if not _CMP[type(op)](left, right):
                return False
            left = right
        return True
    if isinstance(node, ast.Call):
        return _FUNCS[node.func.id](*[_eval(arg, env) for arg in node.args])
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_eval(element, env) for element in node.elts]
    raise ExprError(f"desteklenmeyen yapı: {type(node).__name__}")
