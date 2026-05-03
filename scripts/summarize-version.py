#!/usr/bin/env python3
"""Promote per-scenario extracted artifacts to the version root.

After ``extract.py`` has run for every scenario in versions/<v>/scenarios/,
this script publishes the *baseline* artifacts (system prompt, tool list,
reminders) at versions/<v>/ root so a reader can answer "what does this
version look like?" without descending into a scenario folder.

The baseline is the simplest scenario (``01-bare`` by default — single-turn
``hi`` with no MCP and no skills). An aggregate manifest summarizes
per-scenario stats.

Usage:
    scripts/summarize-version.py 2.1.126 [--baseline 01-bare]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
VERSIONS_DIR = REPO_DIR / "versions"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import dir_for, find_existing_dir  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("version", help="npm version (e.g. 2.1.126); folder lookup uses <date>_<version>")
    p.add_argument("--baseline", default="01-bare")
    args = p.parse_args()

    npm_version = args.version
    existing = find_existing_dir(npm_version)
    dir_name = existing.name if existing else dir_for(npm_version)
    vroot = VERSIONS_DIR / dir_name
    sroot = vroot / "scenarios"
    if not sroot.exists():
        sys.exit(f"no scenarios at {sroot} — run capture+extract first")

    baseline_ext = sroot / args.baseline / "extracted"
    if not baseline_ext.exists():
        sys.exit(
            f"baseline scenario {args.baseline!r} not extracted at {baseline_ext}"
        )

    # Promote baseline files to version root (overwrite each time).
    for fname in (
        "system-prompt.md",
        "user-prompt.md",
        "tools.json",
        "deferred-tools.json",
        "skills.json",
    ):
        src = baseline_ext / fname
        if src.exists():
            shutil.copy2(src, vroot / fname)

    # Aggregate per-scenario stats into one root manifest.
    scenarios = {}
    for scen_dir in sorted(sroot.iterdir()):
        s_path = scen_dir / "extracted" / "stats.json"
        if s_path.exists():
            scenarios[scen_dir.name] = json.loads(s_path.read_text())
        elif (scen_dir / "output.txt").exists():
            text = (scen_dir / "output.txt").read_text()
            ec_path = scen_dir / "exit-code.txt"
            scenarios[scen_dir.name] = {
                "mode": "local",
                "output_chars": len(text),
                "output_lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
                "exit_code": int(ec_path.read_text().strip()) if ec_path.exists() else None,
            }
        else:
            scenarios[scen_dir.name] = {"empty": True, "note": "no captured artifact"}

    baseline = scenarios.get(args.baseline, {})
    aggregate = {
        "version": npm_version,
        "dir_name": dir_name,
        "baseline_scenario": args.baseline,
        "baseline": {
            "models": baseline.get("models"),
            "tool_count": baseline.get("tool_count_first_request"),
            "deferred_tool_count": baseline.get("deferred_tool_count"),
            "mcp_tool_count_advertised": baseline.get("mcp_tool_count_advertised"),
            "mcp_tool_count_deferred": baseline.get("mcp_tool_count_deferred"),
            "system_prompt_chars": baseline.get("system_prompt_chars"),
            "reminder_count": baseline.get("reminder_count"),
        },
        "scenarios": scenarios,
    }
    (vroot / "manifest.json").write_text(json.dumps(aggregate, indent=2) + "\n")

    # Per-scenario summary table for fast at-a-glance review.
    lines = [
        f"# claude-code {npm_version} — capture summary",
        "",
        f"Baseline scenario: `{args.baseline}` (its system-prompt / tools "
        "are mirrored at the version root).",
        "",
        "| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, m in scenarios.items():
        if m.get("mode") == "local":
            lines.append(
                f"| `{name}` | _local_ | — | — | — | — | — | "
                f"{m.get('output_chars')} chars / {m.get('output_lines')} lines | — | — | — | exit {m.get('exit_code')} |"
            )
            continue
        if m.get("empty"):
            lines.append(f"| `{name}` | — | — | — | — | — | — | — | — | — | — | _no API requests_ |")
            continue
        tk = m.get("tokens") or {}
        dur_ms = m.get("duration_ms_total") or 0
        dur = f"{dur_ms / 1000:.1f}s" if dur_ms else "—"
        lines.append(
            f"| `{name}` "
            f"| {m.get('request_count')} "
            f"| {m.get('tool_count_first_request')} "
            f"| {m.get('deferred_tool_count') or 0} "
            f"| {m.get('mcp_tool_count_advertised') or 0} "
            f"| {m.get('mcp_tool_count_deferred') or 0} "
            f"| {m.get('skill_count') or 0} "
            f"| {m.get('system_prompt_chars')} "
            f"| {m.get('reminder_count')} "
            f"| {tk.get('input')} "
            f"| {tk.get('output')} "
            f"| {dur} |"
        )
    lines.append("")
    lines.append("## Models seen across scenarios")
    lines.append("")
    seen_models: set[str] = set()
    for m in scenarios.values():
        for mod in (m.get("models") or []):
            seen_models.add(mod)
    for mod in sorted(seen_models):
        lines.append(f"- `{mod}`")
    (vroot / "stats.md").write_text("\n".join(lines) + "\n")

    print(f"summarized {vroot.relative_to(REPO_DIR)} (baseline: {args.baseline})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
