#!/usr/bin/env python3
"""Generate a markdown diff report between two extracted versions.

Compares the *baseline* artifacts promoted to each version's root
(system-prompt.md, user-prompt.md, tools.json, deferred-tools.json,
skills.json) plus the stdout-capture scenario (01-cli-help).

Per-scenario diffs are intentionally not included — the cross-version surface
that matters is what every session sees, and that lives at the version root.

Output: versions/<to>/diff-from-<from>.md (colocated with the newer version).

Usage:
    scripts/diff-versions.py 2.1.59 2.1.126
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
VERSIONS_DIR = REPO_DIR / "versions"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import dir_for, find_existing_dir, version_from_dir  # noqa: E402

# Stdout-capture scenarios we always include in the diff. `01-cli-help` is the
# CLI surface (`claude --help`).
CLI_SCENARIOS = ("01-cli-help",)


def _resolve_dir(version_or_dir: str) -> str:
    """Accept either an npm version (2.1.126) or a directory name (2026-04-30_2.1.126)."""
    candidate = VERSIONS_DIR / version_or_dir
    if candidate.is_dir():
        return version_or_dir
    existing = find_existing_dir(version_or_dir)
    if existing:
        return existing.name
    return dir_for(version_or_dir)


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def _diff(a: str, b: str, *, label_a: str, label_b: str) -> str:
    if a == b:
        return ""
    lines = difflib.unified_diff(
        a.splitlines(keepends=True),
        b.splitlines(keepends=True),
        fromfile=label_a,
        tofile=label_b,
        n=3,
    )
    return "".join(lines)


def _tool_delta(a: list, b: list, a_def: list[str], b_def: list[str]) -> dict:
    """Compare advertised + deferred tool sets.

    A tool that left the advertised list but is in the new deferred set is
    NOT removed — it's been moved behind ToolSearch. We treat the union of
    advertised+deferred as the version's full tool surface.
    """
    if a is None or b is None:
        return {}
    a_by = {t["name"]: t for t in (a or [])}
    b_by = {t["name"]: t for t in (b or [])}
    a_def_set = set(a_def or [])
    b_def_set = set(b_def or [])
    a_all = set(a_by) | a_def_set
    b_all = set(b_by) | b_def_set
    moved_to_deferred = sorted((set(a_by) - set(b_by)) & b_def_set)
    moved_to_advertised = sorted((set(b_by) - set(a_by)) & a_def_set)
    deferred_added = sorted(b_def_set - a_def_set - set(moved_to_deferred))
    modified = sorted(
        n for n in set(a_by) & set(b_by)
        if json.dumps(a_by[n], sort_keys=True) != json.dumps(b_by[n], sort_keys=True)
    )
    return {
        "added": sorted(b_all - a_all),
        "removed": sorted(a_all - b_all),
        "modified": modified,
        "moved_to_deferred": moved_to_deferred,
        "moved_to_advertised": moved_to_advertised,
        "deferred_added": deferred_added,
    }


_HELP_SECTION_RX = re.compile(r"^([A-Z][a-z]+):\s*$")
_HELP_LINE_RX = re.compile(r"^  ([^\s]+(?:,\s+[^\s]+)?)")


def _parse_cli_help(text: str) -> dict[str, list[str]]:
    """Extract identifier lists from a Commander-style `--help` output."""
    sections: dict[str, list[str]] = {"options": [], "commands": [], "arguments": []}
    current: str | None = None
    for line in text.splitlines():
        m = _HELP_SECTION_RX.match(line.strip())
        if m:
            section = m.group(1).lower()
            current = section if section in sections else None
            continue
        if not current:
            continue
        m = _HELP_LINE_RX.match(line)
        if not m:
            continue
        for token in m.group(1).split(","):
            token = token.strip()
            if current == "options" and token.startswith("-"):
                sections[current].append(token)
            elif current in ("commands", "arguments") and re.match(r"^[a-z]", token):
                sections[current].append(token)
    return sections


def _tools_section(va: str, vb: str, va_label: str, vb_label: str) -> str:
    a_dir = VERSIONS_DIR / va
    b_dir = VERSIONS_DIR / vb
    a_tools = _read_json(a_dir / "tools.json") or []
    b_tools = _read_json(b_dir / "tools.json") or []
    a_def = _read_json(a_dir / "deferred-tools.json") or []
    b_def = _read_json(b_dir / "deferred-tools.json") or []

    delta = _tool_delta(a_tools, b_tools, a_def, b_def)

    a_adv_names = sorted(t["name"] for t in a_tools)
    b_adv_names = sorted(t["name"] for t in b_tools)
    a_def_sorted = sorted(a_def)
    b_def_sorted = sorted(b_def)

    def _signed(av: int, bv: int) -> str:
        d = bv - av
        return f" ({d:+d})" if d else ""

    lines = ["## tools", ""]

    # Counts table — gives the at-a-glance total even when nothing changed.
    lines.append(f"| count | {va_label} | {vb_label} |")
    lines.append("|---|---|---|")
    lines.append(
        f"| advertised | {len(a_adv_names)} | "
        f"{len(b_adv_names)}{_signed(len(a_adv_names), len(b_adv_names))} |"
    )
    lines.append(
        f"| deferred | {len(a_def_sorted)} | "
        f"{len(b_def_sorted)}{_signed(len(a_def_sorted), len(b_def_sorted))} |"
    )
    a_total = len(a_adv_names) + len(a_def_sorted)
    b_total = len(b_adv_names) + len(b_def_sorted)
    lines.append(
        f"| **total** | **{a_total}** | "
        f"**{b_total}**{_signed(a_total, b_total)} |"
    )
    lines.append("")

    if any(delta.values()):
        if delta["added"]:
            lines.append("- **added:** " + ", ".join(f"`{n}`" for n in delta["added"]))
        if delta["removed"]:
            lines.append("- **removed:** " + ", ".join(f"`{n}`" for n in delta["removed"]))
        if delta["moved_to_deferred"]:
            lines.append(
                "- **moved to deferred (now lazy-loaded via ToolSearch):** "
                + ", ".join(f"`{n}`" for n in delta["moved_to_deferred"])
            )
        if delta["moved_to_advertised"]:
            lines.append(
                "- **moved to advertised (no longer deferred):** "
                + ", ".join(f"`{n}`" for n in delta["moved_to_advertised"])
            )
        if delta["deferred_added"]:
            lines.append(
                "- **new deferred tools:** "
                + ", ".join(f"`{n}`" for n in delta["deferred_added"])
            )
        if delta["modified"]:
            lines.append("- **modified:** " + ", ".join(f"`{n}`" for n in delta["modified"]))
        lines.append("")

    # Full list snapshot for the newer version — keeps the diff document
    # self-contained so a reader doesn't have to cross-reference tools.json.
    lines.append("<details><summary>full tool list — {}: {} advertised + {} deferred</summary>\n".format(
        vb_label, len(b_adv_names), len(b_def_sorted),
    ))
    if b_adv_names:
        lines.append("**advertised**\n")
        for n in b_adv_names:
            lines.append(f"- `{n}`")
        lines.append("")
    if b_def_sorted:
        lines.append("**deferred (via ToolSearch)**\n")
        for n in b_def_sorted:
            lines.append(f"- `{n}`")
        lines.append("")
    lines.append("</details>")
    lines.append("")
    return "\n".join(lines)


def _skills_section(va: str, vb: str) -> str:
    sa = _read_json(VERSIONS_DIR / va / "skills.json") or []
    sb = _read_json(VERSIONS_DIR / vb / "skills.json") or []
    sa_by = {s["name"]: s for s in sa}
    sb_by = {s["name"]: s for s in sb}
    added = sorted(set(sb_by) - set(sa_by))
    removed = sorted(set(sa_by) - set(sb_by))
    modified = sorted(
        n for n in set(sa_by) & set(sb_by)
        if sa_by[n].get("description") != sb_by[n].get("description")
    )
    if not (added or removed or modified):
        return ""
    lines = ["## skills", ""]
    if added:
        lines.append("- **added:** " + ", ".join(f"`{n}`" for n in added))
    if removed:
        lines.append("- **removed:** " + ", ".join(f"`{n}`" for n in removed))
    if modified:
        lines.append("- **description changed:** " + ", ".join(f"`{n}`" for n in modified))
    lines.append("")
    return "\n".join(lines)


def _file_diff_section(title: str, a: Path, b: Path, label_a: str, label_b: str) -> str:
    text = _diff(_read(a), _read(b), label_a=label_a, label_b=label_b)
    if not text:
        return ""
    return "## " + title + "\n\n```diff\n" + text.rstrip() + "\n```\n"


def _cli_section(scenario: str, va: str, vb: str, la: str, lb: str) -> str:
    a_path = VERSIONS_DIR / va / "scenarios" / scenario / "output.txt"
    b_path = VERSIONS_DIR / vb / "scenarios" / scenario / "output.txt"
    if not (a_path.exists() and b_path.exists()):
        return ""
    a_out = _read(a_path)
    b_out = _read(b_path)
    if a_out == b_out:
        return ""
    out: list[str] = [f"## cli: `{scenario}`", ""]

    a_parsed = _parse_cli_help(a_out)
    b_parsed = _parse_cli_help(b_out)
    for section, label in (("options", "flags"), ("commands", "commands"), ("arguments", "arguments")):
        a_set = set(a_parsed.get(section, []))
        b_set = set(b_parsed.get(section, []))
        added = sorted(b_set - a_set)
        removed = sorted(a_set - b_set)
        if not (added or removed):
            continue
        out.append(f"### {label}")
        if added:
            out.append("- **added:** " + ", ".join(f"`{n}`" for n in added))
        if removed:
            out.append("- **removed:** " + ", ".join(f"`{n}`" for n in removed))
        out.append("")

    text_diff = _diff(
        a_out, b_out,
        label_a=f"{la}/{scenario}/output.txt",
        label_b=f"{lb}/{scenario}/output.txt",
    )
    out.append("<details><summary>full diff</summary>\n")
    out.append("```diff")
    out.append(text_diff.rstrip())
    out.append("```")
    out.append("</details>\n")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: diff-versions.py <from-version> <to-version>", file=sys.stderr)
        return 1

    va = _resolve_dir(argv[1])
    vb = _resolve_dir(argv[2])
    va_label = version_from_dir(va)
    vb_label = version_from_dir(vb)

    out_path = VERSIONS_DIR / vb / f"diff-from-{va}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts: list[str] = [f"# claude-code: {va_label} → {vb_label}", ""]

    # Manifest delta — small numeric overview.
    ma = _read_json(VERSIONS_DIR / va / "manifest.json") or {}
    mb = _read_json(VERSIONS_DIR / vb / "manifest.json") or {}
    ba = ma.get("baseline") or {}
    bb = mb.get("baseline") or {}
    parts.append("| metric | " + va_label + " | " + vb_label + " |")
    parts.append("|---|---|---|")
    for k in ("models", "tool_count", "deferred_tool_count", "system_prompt_chars", "reminder_count"):
        av, bv = ba.get(k), bb.get(k)
        if isinstance(av, list):
            av = ", ".join(av)
        if isinstance(bv, list):
            bv = ", ".join(bv)
        parts.append(f"| {k} | {av} | {bv} |")
    parts.append("")

    sections = [
        _tools_section(va, vb, va_label, vb_label),
        _skills_section(va, vb),
        _file_diff_section(
            "system prompt",
            VERSIONS_DIR / va / "system-prompt.md",
            VERSIONS_DIR / vb / "system-prompt.md",
            f"{va_label}/system-prompt.md", f"{vb_label}/system-prompt.md",
        ),
        _file_diff_section(
            "user prompt (incl. system-reminder blocks)",
            VERSIONS_DIR / va / "user-prompt.md",
            VERSIONS_DIR / vb / "user-prompt.md",
            f"{va_label}/user-prompt.md", f"{vb_label}/user-prompt.md",
        ),
    ]
    for scen in CLI_SCENARIOS:
        sections.append(_cli_section(scen, va, vb, va_label, vb_label))

    non_empty = [s for s in sections if s]
    if non_empty:
        parts.extend(non_empty)
    else:
        parts.append("_no observable change at the version-root or CLI surface_\n")

    out_path.write_text("\n".join(parts) + ("\n" if not parts[-1].endswith("\n") else ""))
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
