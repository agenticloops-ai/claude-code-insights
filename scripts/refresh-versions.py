#!/usr/bin/env python3
"""Regenerate VERSIONS.md from npm + the upstream CHANGELOG.

Idempotent. Safe to re-run; the file is overwritten in place.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys
import urllib.request

NPM_META_URL = "https://registry.npmjs.org/@anthropic-ai/claude-code"
CHANGELOG_RAW = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
CHANGELOG_URL = "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
NPM_URL = "https://www.npmjs.com/package/@anthropic-ai/claude-code/v"
NPM_BADGE = "https://img.shields.io/badge/npm-cb3837?logo=npm&logoColor=white"
NOTES_BADGE = "https://img.shields.io/badge/changelog-blue?logo=github&logoColor=white"
DIFF_BADGE = "https://img.shields.io/badge/diff-555?logo=git&logoColor=white"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "VERSIONS.md"
VERSIONS_DIR = ROOT / "versions"


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read()


def parse_version(v: str) -> tuple:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$", v)
    if not m:
        return (0, 0, 0, v)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or "~")


def slug(v: str) -> str:
    s = v.lower()
    s = re.sub(r"[^\w\- ]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def scan_diffs() -> dict[str, str]:
    """Map version string -> repo-relative path to its diff-from-*.md, if present."""
    out: dict[str, str] = {}
    if not VERSIONS_DIR.is_dir():
        return out
    for d in VERSIONS_DIR.iterdir():
        if not d.is_dir():
            continue
            # dir name is "<date>_<version>"
        m = re.match(r"^\d{4}-\d{2}-\d{2}_(.+)$", d.name)
        if not m:
            continue
        version = m.group(1)
        diff = next(d.glob("diff-from-*.md"), None)
        if diff is not None:
            out[version] = f"versions/{d.name}/{diff.name}"
    return out


def main() -> int:
    meta = json.loads(fetch(NPM_META_URL))
    times = meta.get("time", {})
    versions = sorted(
        ((v, t) for v, t in times.items() if v not in ("created", "modified")),
        key=lambda x: parse_version(x[0]),
        reverse=True,
    )
    if not versions:
        print("ERROR: no versions found", file=sys.stderr)
        return 1

    changelog = fetch(CHANGELOG_RAW).decode()
    documented = set(re.findall(r"^##\s+([0-9]+\.[0-9]+\.[0-9]+(?:[-.][\w.]+)?)\s*$",
                                 changelog, re.M))
    diffs = scan_diffs()

    lines: list[str] = [
        "# Claude Code Versions",
        "",
        "All published versions of `@anthropic-ai/claude-code` on npm, newest first.",
        "",
        f"- **Total versions:** {len(versions)}",
        f"- **First release:** {min(t for _, t in versions)[:10]}",
        f"- **Latest release:** {max(t for _, t in versions)[:10]}",
        f"- **Source:** [npm registry]({NPM_META_URL})",
        f"- **Upstream changelog:** [{CHANGELOG_URL}]({CHANGELOG_URL})",
        f"- **Generated:** {datetime.date.today().isoformat()}",
        "",
        "Versions without a changelog entry are usually silent patches or pre-1.0 cuts.",
        "",
        "| Version | Released | Changelog | Diff | npm |",
        "|---------|----------|-----------|------|-----|",
    ]
    for v, t in versions:
        date = t[:10]
        notes = (
            f"[![changelog]({NOTES_BADGE})]({CHANGELOG_URL}#{slug(v)})"
            if v in documented else "—"
        )
        diff = (
            f"[![diff]({DIFF_BADGE})]({diffs[v]})"
            if v in diffs else "—"
        )
        npm = f"[![npm]({NPM_BADGE})]({NPM_URL}/{v})"
        lines.append(f"| `{v}` | {date} | {notes} | {diff} | {npm} |")

    OUT.write_text("\n".join(lines) + "\n")
    print(
        f"wrote {OUT.name}: {len(versions)} versions, "
        f"{sum(1 for v, _ in versions if v in documented)} with CHANGELOG entries, "
        f"{len(diffs)} with diff files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
