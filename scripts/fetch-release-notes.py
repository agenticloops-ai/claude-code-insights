#!/usr/bin/env python3
"""Download the upstream CHANGELOG entry for a single version.

Writes versions/<version>/release-notes.md with the section between
``## <version>`` and the next ``## `` heading. If the upstream changelog has
no entry (silent patch), writes a one-line placeholder so the absence is
visible.

Usage:
    scripts/fetch-release-notes.py 2.1.126
"""
from __future__ import annotations

import datetime
import re
import sys
import urllib.request
from pathlib import Path

CHANGELOG_RAW = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
NPM_META = "https://registry.npmjs.org/@anthropic-ai/claude-code"
REPO_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import dir_for, find_existing_dir  # noqa: E402


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read()


def _section(changelog: str, version: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(version)}\s*\n(.*?)(?=^##\s+\S)",
        re.M | re.S,
    )
    m = pattern.search(changelog)
    if not m:
        return None
    return m.group(1).strip()


def _publish_date(version: str) -> str | None:
    try:
        import json

        meta = json.loads(_fetch(NPM_META))
        ts = (meta.get("time") or {}).get(version)
        return ts[:10] if ts else None
    except Exception:
        return None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: fetch-release-notes.py <version>", file=sys.stderr)
        return 1

    version = argv[1]
    existing = find_existing_dir(version)
    dir_name = existing.name if existing else dir_for(version)
    out_dir = REPO_DIR / "versions" / dir_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "release-notes.md"

    changelog = _fetch(CHANGELOG_RAW).decode()
    section = _section(changelog, version)
    published = _publish_date(version)

    lines = [f"# claude-code {version}", ""]
    if published:
        lines.append(f"- **published:** {published}")
    lines.append(
        "- **source:** "
        f"[CHANGELOG.md#{version.replace('.', '')}]"
        f"(https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#{version.replace('.', '')})"
    )
    lines.append(f"- **fetched:** {datetime.date.today().isoformat()}")
    lines.append("")
    if section:
        lines.append(section)
    else:
        lines.append("> No entry in upstream CHANGELOG.md (likely a silent patch).")
    lines.append("")

    out_path.write_text("\n".join(lines))
    status = "with entry" if section else "no entry"
    print(f"wrote {out_path.relative_to(REPO_DIR)} ({status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
