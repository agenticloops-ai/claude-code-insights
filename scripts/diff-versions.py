#!/usr/bin/env python3
"""Generate a markdown diff report between two extracted versions.

Reads versions/<a>/<scenario>/extracted/ and versions/<b>/<scenario>/extracted/
for every shared scenario and writes the comparison to
versions/<b>/diff-from-<a>.md (i.e. the diff is colocated with the *newer*
version's artifacts).

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


def _resolve_dir(version_or_dir: str) -> str:
    """Accept either an npm version (2.1.126) or a directory name (2026-04-30_2.1.126)."""
    candidate = VERSIONS_DIR / version_or_dir
    if candidate.is_dir():
        return version_or_dir
    existing = find_existing_dir(version_or_dir)
    if existing:
        return existing.name
    return dir_for(version_or_dir)


def _scenarios(version: str) -> set[str]:
    base = VERSIONS_DIR / version / "scenarios"
    if not base.exists():
        sys.exit(f"no extracted artifacts at {base}")
    return {
        p.name
        for p in base.iterdir()
        if p.is_dir() and ((p / "extracted").is_dir() or (p / "output.txt").exists())
    }


def _ext(version: str, scenario: str) -> Path:
    return VERSIONS_DIR / version / "scenarios" / scenario / "extracted"


def _scen_dir(version: str, scenario: str) -> Path:
    return VERSIONS_DIR / version / "scenarios" / scenario


def _is_local(version: str, scenario: str) -> bool:
    return (_scen_dir(version, scenario) / "output.txt").exists() and not _ext(version, scenario).exists()


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


def _tool_delta(
    a: list,
    b: list,
    a_def: list[str],
    b_def: list[str],
) -> dict:
    """Compare advertised + deferred tool sets.

    A tool that left the advertised list but is in the new deferred set is
    NOT removed — it's just been moved behind ToolSearch. We treat the union
    of advertised+deferred as the version's full tool surface.
    """
    if a is None or b is None:
        return {"added": [], "removed": [], "modified": [], "deferred_in_b_only": [], "moved_to_deferred": []}

    a_by = {t["name"]: t for t in (a or [])}
    b_by = {t["name"]: t for t in (b or [])}
    a_def_set = set(a_def or [])
    b_def_set = set(b_def or [])

    a_all = set(a_by) | a_def_set
    b_all = set(b_by) | b_def_set

    truly_added = sorted(b_all - a_all)
    truly_removed = sorted(a_all - b_all)
    moved_to_deferred_set = (set(a_by) - set(b_by)) & b_def_set
    moved_to_advertised = sorted((set(b_by) - set(a_by)) & a_def_set)
    deferred_only_in_b = sorted(b_def_set - a_def_set - moved_to_deferred_set)
    moved_to_deferred = sorted(moved_to_deferred_set)

    modified = sorted(
        n
        for n in set(a_by) & set(b_by)
        if json.dumps(a_by[n], sort_keys=True) != json.dumps(b_by[n], sort_keys=True)
    )
    return {
        "added": truly_added,
        "removed": truly_removed,
        "modified": modified,
        "moved_to_deferred": moved_to_deferred,
        "moved_to_advertised": moved_to_advertised,
        "deferred_added": deferred_only_in_b,
    }


_HELP_SECTION_RX = re.compile(r"^([A-Z][a-z]+):\s*$")
_HELP_LINE_RX = re.compile(r"^  ([^\s]+(?:,\s+[^\s]+)?)")


def _parse_cli_help(text: str) -> dict[str, list[str]]:
    """Extract identifier lists from a Commander-style `--help` output.

    Returns ``{"options": [...], "commands": [...], "arguments": [...]}``.
    Identifiers are taken from the first whitespace-delimited token (or
    comma-separated alias pair) of each indented line under the matching
    section. Wrapped description lines are ignored because they don't start
    with exactly two spaces + a flag/command-like token.
    """
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


def _local_section(scenario: str, va: str, vb: str, la: str | None = None, lb: str | None = None) -> str:
    la = la or version_from_dir(va)
    lb = lb or version_from_dir(vb)
    """Diff a local-mode scenario (claude --help, etc.)."""
    out: list[str] = [f"## scenario: `{scenario}` _(local)_", ""]
    a_out = _read(_scen_dir(va, scenario) / "output.txt")
    b_out = _read(_scen_dir(vb, scenario) / "output.txt")
    if a_out == b_out:
        out.append("_no change_")
        out.append("")
        return "\n".join(out)

    out.append(f"- chars: {len(a_out)} → {len(b_out)}")
    out.append(f"- lines: {a_out.count(chr(10))} → {b_out.count(chr(10))}")
    out.append("")

    # Structured added/removed flags + commands when the output looks like
    # a CLI help page.
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
        label_a=f"{la}/scenarios/{scenario}/output.txt",
        label_b=f"{lb}/scenarios/{scenario}/output.txt",
    )
    out.append("### full diff")
    out.append("```diff")
    out.append(text_diff.rstrip())
    out.append("```")
    out.append("")
    return "\n".join(out)


def _scenario_section(scenario: str, va: str, vb: str, la: str | None = None, lb: str | None = None) -> str:
    la = la or version_from_dir(va)
    lb = lb or version_from_dir(vb)
    if _is_local(va, scenario) and _is_local(vb, scenario):
        return _local_section(scenario, va, vb, la, lb)

    a_dir = _ext(va, scenario)
    b_dir = _ext(vb, scenario)

    out: list[str] = [f"## scenario: `{scenario}`", ""]

    ma = _read_json(a_dir / "stats.json")
    mb = _read_json(b_dir / "stats.json")
    if ma and mb:
        out.append("| metric | " + la + " | " + lb + " |")
        out.append("|---|---|---|")
        for k in (
            "request_count",
            "tool_count_first_request",
            "deferred_tool_count",
            "skill_count",
            "system_prompt_chars",
            "user_prompt_chars",
            "reminder_count",
            "duration_ms_total",
        ):
            out.append(f"| {k} | {ma.get(k)} | {mb.get(k)} |")
        for k in ("input", "output", "total"):
            out.append(
                f"| tokens.{k} | {(ma.get('tokens') or {}).get(k)} | {(mb.get('tokens') or {}).get(k)} |"
            )
        out.append(f"| models | {', '.join(ma.get('models') or [])} | {', '.join(mb.get('models') or [])} |")
        out.append("")

    sa = _read_json(a_dir / "skills.json") or []
    sb = _read_json(b_dir / "skills.json") or []
    sa_by = {s["name"]: s for s in sa}
    sb_by = {s["name"]: s for s in sb}
    s_added = sorted(set(sb_by) - set(sa_by))
    s_removed = sorted(set(sa_by) - set(sb_by))
    s_modified = sorted(
        n for n in set(sa_by) & set(sb_by)
        if sa_by[n].get("description") != sb_by[n].get("description")
    )
    if s_added or s_removed or s_modified:
        out.append("### built-in skills")
        if s_added:
            out.append("- **added:** " + ", ".join(f"`{n}`" for n in s_added))
        if s_removed:
            out.append("- **removed:** " + ", ".join(f"`{n}`" for n in s_removed))
        if s_modified:
            out.append("- **description changed:** " + ", ".join(f"`{n}`" for n in s_modified))
        out.append("")

    ta = _read_json(a_dir / "tools.json") or []
    tb = _read_json(b_dir / "tools.json") or []
    a_def = _read_json(a_dir / "deferred-tools.json") or []
    b_def = _read_json(b_dir / "deferred-tools.json") or []
    delta = _tool_delta(ta, tb, a_def, b_def)
    if any(delta.values()):
        out.append("### tools")
        if delta["added"]:
            out.append("- **added:** " + ", ".join(f"`{n}`" for n in delta["added"]))
        if delta["removed"]:
            out.append("- **removed:** " + ", ".join(f"`{n}`" for n in delta["removed"]))
        if delta["moved_to_deferred"]:
            out.append(
                "- **moved to deferred (now lazy-loaded via ToolSearch):** "
                + ", ".join(f"`{n}`" for n in delta["moved_to_deferred"])
            )
        if delta["moved_to_advertised"]:
            out.append(
                "- **moved to advertised (no longer deferred):** "
                + ", ".join(f"`{n}`" for n in delta["moved_to_advertised"])
            )
        if delta["deferred_added"]:
            out.append(
                "- **new deferred tools:** "
                + ", ".join(f"`{n}`" for n in delta["deferred_added"])
            )
        if delta["modified"]:
            out.append("- **modified:** " + ", ".join(f"`{n}`" for n in delta["modified"]))
        out.append("")

    sys_diff = _diff(
        _read(a_dir / "system-prompt.md"),
        _read(b_dir / "system-prompt.md"),
        label_a=f"{la}/system-prompt.md",
        label_b=f"{lb}/system-prompt.md",
    )
    if sys_diff:
        out.append("### system prompt")
        out.append("```diff")
        out.append(sys_diff.rstrip())
        out.append("```")
        out.append("")

    user_diff = _diff(
        _read(a_dir / "user-prompt.md"),
        _read(b_dir / "user-prompt.md"),
        label_a=f"{la}/user-prompt.md",
        label_b=f"{lb}/user-prompt.md",
    )
    if user_diff:
        out.append("### user prompt (incl. system-reminder blocks)")
        out.append("```diff")
        out.append(user_diff.rstrip())
        out.append("```")
        out.append("")

    if len(out) == 2:
        out.append("_no observable change_")
        out.append("")

    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: diff-versions.py <from-version> <to-version>", file=sys.stderr)
        return 1

    # Accept either npm version (2.1.126) or folder name (2026-04-30_2.1.126).
    va = _resolve_dir(argv[1])
    vb = _resolve_dir(argv[2])
    va_label = version_from_dir(va)
    vb_label = version_from_dir(vb)
    scens_a = _scenarios(va)
    scens_b = _scenarios(vb)
    shared = sorted(scens_a & scens_b)
    only_a = sorted(scens_a - scens_b)
    only_b = sorted(scens_b - scens_a)

    out_path = VERSIONS_DIR / vb / f"diff-from-{va}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts: list[str] = [
        f"# claude-code: {va_label} → {vb_label}",
        "",
        f"- shared scenarios: {len(shared)}",
        f"- only in {va_label}: {only_a or '—'}",
        f"- only in {vb_label}: {only_b or '—'}",
        "",
    ]
    for s in shared:
        parts.append(_scenario_section(s, va, vb, va_label, vb_label))

    out_path.write_text("\n".join(parts) + "\n")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
