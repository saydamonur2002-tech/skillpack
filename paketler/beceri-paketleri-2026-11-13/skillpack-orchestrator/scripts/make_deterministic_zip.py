#!/usr/bin/env python3
"""Create a deterministic ZIP of a skill pack directory.
Uses fixed timestamps and sorted file order so the same content always produces the same hash.
"""
import argparse
import hashlib
import os
import zipfile
from pathlib import Path

FIXED_TIME = (2026, 1, 1, 0, 0, 0)

def make_deterministic_zip(src_dir: Path, zip_path: Path):
    src_dir = src_dir.resolve()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            dirs.sort()
            for name in sorted(files):
                full = Path(root) / name
                arcname = full.relative_to(src_dir).as_posix()
                info = zipfile.ZipInfo(arcname)
                info.date_time = FIXED_TIME
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16  # regular file
                with open(full, "rb") as f:
                    zf.writestr(info, f.read())
    # compute hash
    h = hashlib.sha256()
    with open(zip_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="skill pack directory")
    parser.add_argument("--out", help="output zip path (default: <src>.zip)")
    args = parser.parse_args()

    src = Path(args.src)
    if not src.is_dir():
        raise SystemExit(f"Not a directory: {src}")
    out = Path(args.out) if args.out else src.with_suffix(".zip")
    digest = make_deterministic_zip(src, out)
    print(f"Created {out}")
    print(f"SHA256: {digest}")

if __name__ == "__main__":
    main()
