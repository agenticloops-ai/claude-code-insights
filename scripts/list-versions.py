#!/usr/bin/env python3
"""Print every documented (CHANGELOG-entry) claude-code version, oldest first.

"Documented" means the version appears as a top-level heading in the upstream
CHANGELOG.md (same criterion as the [changelog] badge in VERSIONS.md).

Usage:
    scripts/list-versions.py              # one version per line, oldest first
    scripts/list-versions.py --with-date  # <YYYY-MM-DD>\t<version>
    scripts/list-versions.py --all        # all npm versions, not just documented ones
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import _fetch_npm_times  # noqa: E402

CHANGELOG_RAW = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"


def parse_version(v: str) -> tuple:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$", v)
    if not m:
        return (0, 0, 0, v)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or "~")


def documented_versions() -> set[str]:
    with urllib.request.urlopen(CHANGELOG_RAW, timeout=30) as r:
        changelog = r.read().decode()
    return set(re.findall(r"^##\s+([0-9]+\.[0-9]+\.[0-9]+(?:[-.][\w.]+)?)\s*$",
                          changelog, re.M))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--with-date", action="store_true",
                        help="prefix each version with its release date")
    parser.add_argument("--all", action="store_true",
                        help="include all npm versions, not just documented ones")
    args = parser.parse_args()

    times = _fetch_npm_times()
    documented = set() if args.all else documented_versions()

    pairs = sorted(
        ((date, v) for v, date in times.items() if args.all or v in documented),
        key=lambda x: (x[0], parse_version(x[1])),
    )

    for date, v in pairs:
        if args.with_date:
            print(f"{date}\t{v}")
        else:
            print(v)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
