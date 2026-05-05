#!/usr/bin/env python3
"""Mine every versions/<v>/diff-from-*.md plus manifest.json into structured
timeline data for the evolution research doc.

Outputs to research/data/:
  tools.csv               every tool add / remove / move event
  skills.csv              every skill add / remove / description change
  cli.csv                 every CLI flag / command / argument change
  prompts.csv             system + user prompt diff sizes per version
  manifest-stats.csv      per-version manifest stats (counts, models, tokens)
  milestones.json         coarse-grained "first appearance" of every entity
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VERSIONS = REPO / "versions"
OUT = REPO / "research" / "data"
OUT.mkdir(parents=True, exist_ok=True)


def _ver_from_dir(d: str) -> tuple[str, str]:
    """`2026-04-30_2.1.126` -> (`2026-04-30`, `2.1.126`)."""
    date, _, ver = d.partition("_")
    return date, ver


def _ver_key(v: str) -> tuple:
    return tuple(int(x) if x.isdigit() else 0 for x in v.split("."))


def _section(text: str, header: str) -> str:
    """Extract one ## <header> ... section up to the next ## header."""
    rx = re.compile(rf"^## {re.escape(header)}\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
    m = rx.search(text)
    return m.group(1) if m else ""


def _bullet_list(line: str) -> list[str]:
    """Pull `name` tokens from a "- **added:** `a`, `b`, `c`" bullet."""
    return re.findall(r"`([^`]+)`", line)


def _parse_tools_section(sec: str) -> dict[str, list[str]]:
    out = {
        "added": [], "removed": [], "modified": [],
        "moved_to_deferred": [], "moved_to_advertised": [],
        "deferred_added": [],
    }
    for line in sec.splitlines():
        s = line.strip()
        if s.startswith("- **added:**"):
            out["added"] = _bullet_list(s)
        elif s.startswith("- **removed:**"):
            out["removed"] = _bullet_list(s)
        elif s.startswith("- **modified:**"):
            out["modified"] = _bullet_list(s)
        elif s.startswith("- **moved to deferred"):
            out["moved_to_deferred"] = _bullet_list(s)
        elif s.startswith("- **moved to advertised"):
            out["moved_to_advertised"] = _bullet_list(s)
        elif s.startswith("- **new deferred tools:**"):
            out["deferred_added"] = _bullet_list(s)
    return out


def _parse_skills_section(sec: str) -> dict[str, list[str]]:
    out = {"added": [], "removed": [], "description_changed": []}
    for line in sec.splitlines():
        s = line.strip()
        if s.startswith("- **added:**"):
            out["added"] = _bullet_list(s)
        elif s.startswith("- **removed:**"):
            out["removed"] = _bullet_list(s)
        elif s.startswith("- **description changed:**"):
            out["description_changed"] = _bullet_list(s)
    return out


_CLI_HEADER_RX = re.compile(r"^### (flags|commands|arguments)\s*$", re.MULTILINE)


def _parse_cli_section(sec: str) -> dict[str, dict[str, list[str]]]:
    """Returns {kind: {added:[…], removed:[…]}} for flags/commands/arguments."""
    out = {k: {"added": [], "removed": []} for k in ("flags", "commands", "arguments")}
    parts = _CLI_HEADER_RX.split(sec)
    # parts is [pre, kind1, body1, kind2, body2, …]
    for i in range(1, len(parts), 2):
        kind = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        for line in body.splitlines():
            s = line.strip()
            if s.startswith("- **added:**"):
                out[kind]["added"] = _bullet_list(s)
            elif s.startswith("- **removed:**"):
                out[kind]["removed"] = _bullet_list(s)
    return out


def _diff_size(sec: str) -> tuple[int, int]:
    """Count + and - lines inside the ```diff fences. Returns (added, removed)."""
    in_diff = False
    plus = minus = 0
    for line in sec.splitlines():
        if line.startswith("```diff"):
            in_diff = True
            continue
        if line.startswith("```") and in_diff:
            in_diff = False
            continue
        if not in_diff:
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            plus += 1
        elif line.startswith("-"):
            minus += 1
    return plus, minus


def main() -> int:
    pairs: list[tuple[str, str, str, str, Path]] = []
    for vdir in sorted(p for p in VERSIONS.iterdir() if p.is_dir()):
        date, ver = _ver_from_dir(vdir.name)
        for diff in sorted(vdir.glob("diff-from-*.md")):
            prev_dir = diff.stem[len("diff-from-"):]
            prev_date, prev_ver = _ver_from_dir(prev_dir)
            pairs.append((date, ver, prev_date, prev_ver, diff))

    tools_rows: list[dict] = []
    skills_rows: list[dict] = []
    cli_rows: list[dict] = []
    prompt_rows: list[dict] = []

    # Track first-appearance of each tool / skill / flag / command for milestones.
    first_seen: dict[str, dict[str, dict]] = {
        "tool": {}, "skill": {}, "flag": {}, "command": {}, "argument": {},
    }

    def _record_first(kind: str, name: str, date: str, ver: str, diff_path: Path) -> None:
        bucket = first_seen[kind]
        if name in bucket:
            return
        bucket[name] = {
            "name": name, "first_seen_date": date, "first_seen_version": ver,
            "diff": str(diff_path.relative_to(REPO)),
        }

    for date, ver, prev_date, prev_ver, diff in pairs:
        text = diff.read_text()

        # tools
        tools_sec = _section(text, "tools")
        if tools_sec:
            d = _parse_tools_section(tools_sec)
            for kind, names in d.items():
                for n in names:
                    tools_rows.append({
                        "date": date, "version": ver,
                        "prev_date": prev_date, "prev_version": prev_ver,
                        "change": kind, "name": n,
                        "diff": str(diff.relative_to(REPO)),
                    })
            for n in d["added"]:
                _record_first("tool", n, date, ver, diff)

        # skills
        skills_sec = _section(text, "skills")
        if skills_sec:
            d = _parse_skills_section(skills_sec)
            for kind, names in d.items():
                for n in names:
                    skills_rows.append({
                        "date": date, "version": ver,
                        "prev_date": prev_date, "prev_version": prev_ver,
                        "change": kind, "name": n,
                        "diff": str(diff.relative_to(REPO)),
                    })
            for n in d["added"]:
                _record_first("skill", n, date, ver, diff)

        # cli
        cli_sec = _section(text, "cli: `01-cli-help`")
        if cli_sec:
            d = _parse_cli_section(cli_sec)
            for kind, deltas in d.items():
                for change, names in deltas.items():
                    for n in names:
                        cli_rows.append({
                            "date": date, "version": ver,
                            "prev_date": prev_date, "prev_version": prev_ver,
                            "kind": kind, "change": change, "name": n,
                            "diff": str(diff.relative_to(REPO)),
                        })
                singular = {"flags": "flag", "commands": "command", "arguments": "argument"}[kind]
                for n in deltas["added"]:
                    _record_first(singular, n, date, ver, diff)

        # prompt diffs (sizes only)
        sys_sec = _section(text, "system prompt")
        usr_sec = _section(text, "user prompt (incl. system-reminder blocks)")
        sp, sm = _diff_size(sys_sec) if sys_sec else (0, 0)
        up, um = _diff_size(usr_sec) if usr_sec else (0, 0)
        prompt_rows.append({
            "date": date, "version": ver,
            "prev_date": prev_date, "prev_version": prev_ver,
            "sys_added_lines": sp, "sys_removed_lines": sm, "sys_net": sp - sm,
            "usr_added_lines": up, "usr_removed_lines": um, "usr_net": up - um,
            "diff": str(diff.relative_to(REPO)),
        })

    # manifest stats per version (independent of diff)
    manifest_rows: list[dict] = []
    for vdir in sorted(p for p in VERSIONS.iterdir() if p.is_dir()):
        date, ver = _ver_from_dir(vdir.name)
        mf = vdir / "manifest.json"
        if not mf.exists():
            continue
        try:
            m = json.loads(mf.read_text())
        except Exception:
            continue
        b = m.get("baseline") or {}
        manifest_rows.append({
            "date": date, "version": ver,
            "models": "|".join(b.get("models") or []),
            "tool_count": b.get("tool_count"),
            "deferred_tool_count": b.get("deferred_tool_count"),
            "mcp_advertised": b.get("mcp_tool_count_advertised"),
            "mcp_deferred": b.get("mcp_tool_count_deferred"),
            "system_prompt_chars": b.get("system_prompt_chars"),
            "user_prompt_chars": b.get("user_prompt_chars"),
            "skill_count": b.get("skill_count"),
            "reminder_count": b.get("reminder_count"),
        })

    def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
        with path.open("w") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"wrote {path.relative_to(REPO)} ({len(rows)} rows)")

    _write_csv(OUT / "tools.csv", tools_rows,
               ["date", "version", "prev_date", "prev_version", "change", "name", "diff"])
    _write_csv(OUT / "skills.csv", skills_rows,
               ["date", "version", "prev_date", "prev_version", "change", "name", "diff"])
    _write_csv(OUT / "cli.csv", cli_rows,
               ["date", "version", "prev_date", "prev_version", "kind", "change", "name", "diff"])
    _write_csv(OUT / "prompts.csv", prompt_rows,
               ["date", "version", "prev_date", "prev_version",
                "sys_added_lines", "sys_removed_lines", "sys_net",
                "usr_added_lines", "usr_removed_lines", "usr_net", "diff"])
    _write_csv(OUT / "manifest-stats.csv", manifest_rows,
               ["date", "version", "models", "tool_count", "deferred_tool_count",
                "mcp_advertised", "mcp_deferred", "system_prompt_chars",
                "user_prompt_chars", "skill_count", "reminder_count"])

    (OUT / "milestones.json").write_text(json.dumps(first_seen, indent=2) + "\n")
    print(f"wrote {(OUT / 'milestones.json').relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
