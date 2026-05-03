"""Folder-naming helpers shared across the pipeline.

Captured artifacts live under `versions/<release-date>_<npm-version>/` so a
plain `ls` sorts chronologically. This module owns the conversion in both
directions plus a tiny disk cache of npm publish dates so we don't hit the
registry on every script invocation.

CLI form (used by bash callers):
    python3 scripts/_paths.py dir_for 2.1.126   -> "2026-04-30_2.1.126"
    python3 scripts/_paths.py version_from_dir 2026-04-30_2.1.126 -> "2.1.126"
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
VERSIONS_DIR = REPO_DIR / "versions"
CACHE_PATH = VERSIONS_DIR / ".npm-times.json"
NPM_META_URL = "https://registry.npmjs.org/@anthropic-ai/claude-code"


def _load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text())
    except Exception:
        return {}


def _save_cache(d: dict[str, str]) -> None:
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")


def _fetch_npm_times() -> dict[str, str]:
    with urllib.request.urlopen(NPM_META_URL, timeout=30) as r:
        meta = json.loads(r.read())
    return {v: ts[:10] for v, ts in (meta.get("time") or {}).items() if v not in ("created", "modified")}


def release_date(version: str) -> str:
    """Return YYYY-MM-DD for the given npm version, fetching/caching as needed."""
    cache = _load_cache()
    if version not in cache:
        cache.update(_fetch_npm_times())
        _save_cache(cache)
    if version not in cache:
        raise SystemExit(f"unknown npm version: {version}")
    return cache[version]


def dir_for(version: str) -> str:
    """Folder name for a version: '<date>_<version>'."""
    return f"{release_date(version)}_{version}"


def find_existing_dir(version: str) -> Path | None:
    """Find an already-created versions/<date>_<version>/ dir without hitting npm."""
    if not VERSIONS_DIR.exists():
        return None
    matches = list(VERSIONS_DIR.glob(f"*_{version}"))
    return matches[0] if matches else None


def version_from_dir(name: str) -> str:
    """Inverse of dir_for: '<date>_<version>' -> '<version>'."""
    if "_" not in name:
        return name
    return name.split("_", 1)[1]


def _main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: _paths.py {dir_for|version_from_dir|release_date} <arg>", file=sys.stderr)
        return 1
    cmd, arg = argv[1], argv[2]
    fn = {"dir_for": dir_for, "version_from_dir": version_from_dir, "release_date": release_date}.get(cmd)
    if not fn:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 1
    print(fn(arg))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
