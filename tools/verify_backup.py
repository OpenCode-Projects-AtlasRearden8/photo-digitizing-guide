#!/usr/bin/env python3
"""Verify a backup copy of the photo archive matches the masters.

Compares two folder trees file-by-file using SHA-256 checksums.
Standard library only; no accounts, no network.

Usage:
    python3 tools/verify_backup.py /path/to/masters /path/to/backup

Exit status 0 = backup verified, 1 = mismatches found.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

CHUNK = 1024 * 1024


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(CHUNK):
            h.update(chunk)
    return h.hexdigest()


def relative_files(root: Path) -> dict[str, Path]:
    return {str(p.relative_to(root)): p for p in root.rglob("*") if p.is_file()}


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1

    masters, backup = Path(sys.argv[1]), Path(sys.argv[2])
    if not masters.is_dir() or not backup.is_dir():
        print("Both paths must be existing directories.")
        return 1

    src = relative_files(masters)
    dst = relative_files(backup)

    problems = 0
    missing = sorted(set(src) - set(dst))
    extra = sorted(set(dst) - set(src))
    common = sorted(set(src) & set(dst))

    for rel in missing:
        print(f"MISSING in backup: {rel}")
        problems += 1
    for rel in extra:
        print(f"EXTRA in backup:   {rel}")
        problems += 1

    mismatched = 0
    for rel in common:
        if sha256(src[rel]) != sha256(dst[rel]):
            print(f"MISMATCH:          {rel}")
            mismatched += 1
    problems += mismatched

    print(f"\nChecked {len(common)} files: "
          f"{len(common) - mismatched} identical, {mismatched} mismatched, "
          f"{len(missing)} missing, {len(extra)} extra.")

    if problems:
        print("Backup does NOT match masters.")
        return 1
    print("Backup verified: every file matches the masters byte-for-byte.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
