"""Shared Skillpack runtime (game pack): Python standard library plus jsonschema.

Privacy: this module never logs, prints or stores input contents. Validation
errors name the field and the failed rule, never the submitted value.
"""
import json, math, os, signal, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 65536
SPEC = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
FILE_INPUTS = bool(SPEC.get("budget", {}).get("file_inputs"))


def _env_int(name, default, lo, hi):
    try:
        value = int(os.environ.get(name, default))
    except ValueError:
        value = default
    return max(lo, min(hi, value))


# Only packs that read files may raise their timeout (SKILLPACK_TIMEOUT_SECONDS, 1-120 s).
TIMEOUT = _env_int("SKILLPACK_TIMEOUT_SECONDS", 10, 1, 120) if FILE_INPUTS else 10
MAX_FILE_BYTES = _env_int("SKILLPACK_MAX_FILE_MB", 20, 1, 200) * 1048576


def fail(message, code="INVALID_INPUT"):
    return {"ok": False, "error": {"code": code, "message": str(message)[:500]}}


def finite(v, depth=0):
    if depth > 30:
        raise ValueError("JSON nesting exceeds 30 levels")
    if isinstance(v, float) and not math.isfinite(v):
        raise ValueError("Non-finite number")
    if isinstance(v, dict):
        for x in v.values():
            finite(x, depth + 1)
    if isinstance(v, list):
        for x in v:
            finite(x, depth + 1)


def _describe(error):
    where = "/".join(str(x) for x in error.absolute_path) or "(root)"
    if error.validator in ("required", "additionalProperties", "propertyNames"):
        return "Input rejected at " + where + ": " + error.message[:300]
    rule = error.validator
    hint = ""
    if rule == "enum" and len(json.dumps(error.validator_value)) < 300:
        hint = " (allowed: " + ", ".join(json.dumps(x) for x in error.validator_value) + ")"
    elif rule in ("type", "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "minLength", "maxLength", "minItems", "maxItems", "const"):
        hint = " (" + rule + ": " + json.dumps(error.validator_value)[:80] + ")"
    return "Input rejected at " + where + ": failed '" + str(rule) + "' rule" + hint


def validate(v):
    finite(v)
    if len(json.dumps(v, allow_nan=False, separators=(",", ":"), ensure_ascii=False).encode()) > MAX_BYTES:
        raise ValueError("Input exceeds 65536 bytes")
    errors = sorted(Draft202012Validator(SPEC["inputs"]).iter_errors(v), key=lambda e: (len(e.absolute_path), list(map(str, e.absolute_path))))
    if errors:
        raise ValueError(_describe(errors[0]))
    return v


def allowed_roots():
    raw = os.environ.get("SKILLPACK_FILES_DIR", "")
    return [Path(x).expanduser().resolve() for x in raw.split(os.pathsep) if x.strip()]


def read_input_file(path_text):
    """Read one file chosen by the human inside SKILLPACK_FILES_DIR; size-capped; never logged."""
    if not FILE_INPUTS:
        raise ValueError("This pack does not read files")
    roots = allowed_roots()
    if not roots:
        raise ValueError("File input is disabled: set SKILLPACK_FILES_DIR to the folder(s) this tool may read")
    p = Path(path_text).expanduser()
    if not p.is_absolute():
        p = roots[0] / p
    try:
        p = p.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ValueError("File not found inside SKILLPACK_FILES_DIR") from None
    if not any(p == r or r in p.parents for r in roots):
        raise ValueError("File is outside SKILLPACK_FILES_DIR")
    if not p.is_file():
        raise ValueError("Path is not a regular file")
    size = p.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValueError("File is %d bytes; the limit is %d bytes (SKILLPACK_MAX_FILE_MB)" % (size, MAX_FILE_BYTES))
    with p.open("rb") as f:
        data = f.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("File grew beyond the size limit while reading")
    return data, p.name


def pairs(xs):
    d = {}
    for k, v in xs:
        if k in d:
            raise ValueError("Duplicate JSON key: " + k[:60])
        d[k] = v
    return d


def reject_constant(x):
    raise ValueError("Invalid JSON number: " + x)


def cli(calculate):
    def alarm(*_):
        raise TimeoutError("Calculation exceeded %d seconds" % TIMEOUT)
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(TIMEOUT)
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Input exceeds 65536 bytes")
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject_constant)
        result = calculate(validate(value))
        finite(result)
        answer = {"ok": True, "result": result}
    except TimeoutError as e:
        answer = fail(e, "TIMEOUT")
    except RecursionError:
        answer = fail("Input too deeply nested", "INVALID_INPUT")
    except Exception as e:
        answer = fail(e)
    finally:
        signal.alarm(0)
    sys.stdout.buffer.write((json.dumps(answer, allow_nan=False, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8"))
    sys.stdout.flush()
    return 0 if answer["ok"] else 2
