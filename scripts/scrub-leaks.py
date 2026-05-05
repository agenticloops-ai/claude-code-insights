#!/usr/bin/env python3
"""Strip leaked claude.ai connector tool names and PII from captured artifacts.

The capture sandbox used to surface the auth account's claude.ai-attached
MCP connectors (mcp__claude_ai_*) and personal MCP plugins (mcp__plugin_*)
in the deferred-tools list of the first user message — and the harness
also injects the OAuth account email into a `# userEmail` system-reminder
context block. Both leak into raw request/response/SSE files and the
agentlens session dumps committed under versions/.

This script rewrites those files in place at the byte level. It targets
the literal patterns and is safe to re-run (idempotent). JSON files stay
JSON-valid because both the leaked tool names and email appear inside
already-escaped string values; removing them doesn't disturb structure.

Usage:
    scripts/scrub-leaks.py                      # all of versions/
    scripts/scrub-leaks.py versions/<dir> ...   # specific dirs/files
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Match a leaked tool name in any of the contexts it appears across our
# capture artifacts. Order matters — the most-specific (and most-greedy)
# alternative comes first so escape sequences are consumed cleanly.
#
#   mcp__claude_ai_<Server>__<tool-name>
#   mcp__plugin_<plugin>__<tool-name>
#
# Contexts:
#   1) JSON-escaped newline runs ("\\n", "\\\\n", …) before the name —
#      \\+n? consumes any non-zero backslash run plus optional 'n'.
#   2) Real newline plus optional diff/markdown prefix ("+", "-", " ").
#   3) Bare name as a fallback for SSE chunks that split a list across
#      events and leave fragments without a clean leading separator.
# Match the well-known prefix plus whatever follows. The greedy [\w\-]*
# and repeating (?:__[\w\-]*)* let us catch SSE chunks where a streamed
# tool name was cut off mid-string ("mcp__claude_ai_Canva", "mcp__claude_ai_")
# as well as the full canonical form ("mcp__claude_ai_Canva__cancel-editing").
_TOOL_CORE = r"mcp__(?:claude_ai|plugin)_?[\w\-]*(?:__[\w\-]*)*"
LEAK_TOOL_RX = re.compile(
    rf"\\+n?{_TOOL_CORE}"
    rf"|\n[+\- ]*{_TOOL_CORE}"
    rf"|{_TOOL_CORE}"
)

# Same email regex extract.py uses, so scrubbed values match the
# placeholder already present in extracted artifacts.
EMAIL_RX = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
EMAIL_PLACEHOLDER = "<USER_EMAIL>"

# File suffixes we touch. Everything else under versions/ (binary blobs,
# images) is ignored.
TEXT_SUFFIXES = {".json", ".md", ".txt", ".jsonl"}


def scrub(text: str) -> str:
    text = LEAK_TOOL_RX.sub("", text)
    text = EMAIL_RX.sub(EMAIL_PLACEHOLDER, text)
    return text


def scrub_file(path: Path) -> bool:
    """Rewrite path if it changes. Returns True iff the file was modified."""
    try:
        original = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    cleaned = scrub(original)
    if cleaned == original:
        return False
    path.write_text(cleaned, encoding="utf-8")
    return True


def iter_targets(roots: list[Path]):
    for root in roots:
        if root.is_file():
            if root.suffix in TEXT_SUFFIXES:
                yield root
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix in TEXT_SUFFIXES:
                yield p


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scrub. Defaults to versions/ "
        "relative to the repo root.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing.",
    )
    args = parser.parse_args(argv[1:])

    if args.paths:
        # Reject empty / "." / "/" — those silently scrub the whole repo (or
        # filesystem). Empty strings reach here when a caller passes "$VAR"
        # with VAR unset, which once cost us a stray edit to a tracked doc.
        for p in args.paths:
            if not p or p in (".", "/", "./"):
                print(
                    f"refusing to scrub overly-broad path {p!r}; "
                    "pass an explicit subdir",
                    file=sys.stderr,
                )
                return 2
        roots = [Path(p).resolve() for p in args.paths]
    else:
        repo_root = Path(__file__).resolve().parent.parent
        roots = [repo_root / "versions"]
        if not roots[0].exists():
            print(f"default root {roots[0]} not found", file=sys.stderr)
            return 2

    per_version_changed: dict[str, int] = {}
    total_changed = 0
    total_scanned = 0

    for path in iter_targets(roots):
        total_scanned += 1
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        cleaned = scrub(original)
        if cleaned == original:
            continue
        if not args.dry_run:
            path.write_text(cleaned, encoding="utf-8")
        total_changed += 1
        # Bucket by versions/<dir> for the summary.
        parts = path.parts
        try:
            i = parts.index("versions")
            key = parts[i + 1] if i + 1 < len(parts) else "<root>"
        except ValueError:
            key = "<other>"
        per_version_changed[key] = per_version_changed.get(key, 0) + 1

    verb = "would modify" if args.dry_run else "modified"
    for v in sorted(per_version_changed):
        print(f"{verb} {per_version_changed[v]:4d} files in {v}")
    print(f"{verb} {total_changed} of {total_scanned} files total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
