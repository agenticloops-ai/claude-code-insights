#!/usr/bin/env python3
"""Promote per-scenario extracted artifacts to the version root.

After ``extract.py`` has run for every scenario in versions/<v>/scenarios/,
this script publishes the *baseline* artifacts (system prompt, tool list,
reminders) at versions/<v>/ root so a reader can answer "what does this
version look like?" without descending into a scenario folder.

The baseline is the simplest scenario (``02-bare`` by default — single-turn
``hi`` with no MCP and no skills). An aggregate manifest summarizes
per-scenario stats.

Usage:
    scripts/summarize-version.py 2.1.126 [--baseline 02-bare]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
VERSIONS_DIR = REPO_DIR / "versions"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import dir_for, find_existing_dir  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("version", help="npm version (e.g. 2.1.126); folder lookup uses <date>_<version>")
    p.add_argument("--baseline", default="02-bare")
    args = p.parse_args()

    npm_version = args.version
    existing = find_existing_dir(npm_version)
    dir_name = existing.name if existing else dir_for(npm_version)
    vroot = VERSIONS_DIR / dir_name
    sroot = vroot / "scenarios"
    if not sroot.exists():
        sys.exit(f"no scenarios at {sroot} — run capture+extract first")

    baseline_dir = sroot / args.baseline
    if not (baseline_dir / "stats.json").exists():
        sys.exit(
            f"baseline scenario {args.baseline!r} not extracted at {baseline_dir}"
        )

    # Promote baseline files to version root (overwrite each time).
    for fname in (
        "system-prompt.md",
        "user-prompt.md",
        "tools.json",
        "deferred-tools.json",
        "skills.json",
    ):
        src = baseline_dir / fname
        if src.exists():
            shutil.copy2(src, vroot / fname)

    # Aggregate per-scenario stats into one root manifest.
    scenarios = {}
    for scen_dir in sorted(sroot.iterdir()):
        s_path = scen_dir / "stats.json"
        if s_path.exists():
            scenarios[scen_dir.name] = json.loads(s_path.read_text())
        elif (scen_dir / "output.txt").exists():
            text = (scen_dir / "output.txt").read_text()
            ec_path = scen_dir / "exit-code.txt"
            entry = {
                "mode": "local",
                "output_chars": len(text),
                "output_lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
                "exit_code": int(ec_path.read_text().strip()) if ec_path.exists() else None,
            }
            scenarios[scen_dir.name] = entry
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
            # CLI introspection scenarios (e.g. `claude --help`) aren't model
            # interactions, so they don't belong in the per-scenario stats table.
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

    # Diffs are derived state — regenerate any that reference this version so
    # a scrubber change, recapture, or extraction-logic update doesn't leave
    # stale `diff-from-*.md` files pointing at content this version no longer has.
    regenerated = _regen_touching_diffs(dir_name, npm_version)
    if regenerated:
        print(f"regenerated {len(regenerated)} diff(s) touching {npm_version}: "
              + ", ".join(regenerated))
    return 0


def _regen_touching_diffs(dir_name: str, npm_version: str) -> list[str]:
    """Re-run diff-versions.py for every existing diff file where this
    version appears on either side. Skips pairs whose other side is a
    release-notes-only stub (no manifest.json) — diff-versions.py refuses
    those, and we don't want to delete an out-of-band artifact silently."""
    script = Path(__file__).resolve().parent / "diff-versions.py"
    pairs: set[tuple[str, str]] = set()
    # This version's own diff-from-* files (uses npm_version as `to`).
    for f in (VERSIONS_DIR / dir_name).glob("diff-from-*.md"):
        from_dir = f.stem[len("diff-from-"):]
        pairs.add((from_dir.split("_", 1)[-1], npm_version))
    # Other versions whose diff references this version as `from`.
    suffix_token = dir_name  # diff-from-<full-dir-name>.md
    for d in VERSIONS_DIR.iterdir():
        if not d.is_dir() or d.name == dir_name:
            continue
        for f in d.glob(f"diff-from-{suffix_token}.md"):
            pairs.add((npm_version, d.name.split("_", 1)[-1]))
    regenerated: list[str] = []
    for from_ver, to_ver in sorted(pairs):
        result = subprocess.run(
            [sys.executable, str(script), from_ver, to_ver],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            regenerated.append(f"{from_ver}->{to_ver}")
        else:
            # Surface the refusal/error but don't fail summarize.
            err = (result.stderr or result.stdout).strip()
            print(f"warn: diff {from_ver}->{to_ver} skipped: {err}", file=sys.stderr)
    return regenerated


if __name__ == "__main__":
    raise SystemExit(main())
