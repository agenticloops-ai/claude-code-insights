#!/usr/bin/env python3
"""Extract version-comparable artifacts from an agentlens capture.

Reads versions/<version>/scenarios/<scenario>/raw/<timestamp>/<scenario>.json
and writes canonical artifacts into versions/<version>/scenarios/<scenario>/extracted/.
The split-out files are designed to diff cleanly between releases.

Usage:
    scripts/extract.py versions/2.1.126/scenarios/01-bare
    scripts/extract.py versions/2.1.126/scenarios/01-bare/raw/2026-05-03T05-15-45

The argument can be the scenario dir (most recent raw capture is picked) or
a specific timestamped raw capture dir.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import version_from_dir  # noqa: E402


def _resolve_capture_dir(arg: Path) -> Path:
    """Find the timestamped agentlens capture dir.

    Accepts either:
    - the timestamped dir itself (versions/<v>/<s>/raw/<ts>/)
    - the scenario's raw/ dir (versions/<v>/<s>/raw/) — picks newest ts
    - the scenario dir (versions/<v>/<s>/) — uses raw/ subdir
    """
    if not arg.exists():
        sys.exit(f"capture dir not found: {arg}")
    if (arg / "raw").is_dir() and any((arg / "raw").iterdir()):
        arg = arg / "raw"
    json_files = [p for p in arg.glob("*.json") if p.parent.name != "raw"]
    if json_files:
        return arg
    candidates = sorted([p for p in arg.iterdir() if p.is_dir()])
    if not candidates:
        sys.exit(f"no timestamped subdir in {arg}")
    return candidates[-1]


def _load_session(capture_dir: Path) -> dict:
    json_files = list(capture_dir.glob("*.json"))
    json_files = [p for p in json_files if not p.parent.name == "raw"]
    if not json_files:
        sys.exit(f"no session.json in {capture_dir}")
    return json.loads(json_files[0].read_text())


def _system_prompt_text(prompt: Any) -> str:
    if prompt is None:
        return ""
    if isinstance(prompt, str):
        return prompt
    if isinstance(prompt, list):
        out = []
        for b in prompt:
            if isinstance(b, dict):
                out.append(b.get("text", ""))
            else:
                out.append(str(b))
        return "\n\n".join(out)
    return str(prompt)


def _scrub_volatile(text: str) -> str:
    """Remove per-run volatile values so prompts diff cleanly across runs.

    Also redacts personally-identifying values (email, account UUIDs) so the
    extracted artifacts are safe to commit.
    """
    # Cache-busters / billing fingerprints in the leading header line.
    text = re.sub(r"^x-anthropic-billing-header:.*\n", "", text, flags=re.M)
    text = re.sub(r"cch=\d+", "cch=<REDACTED>", text)
    # Session / account UUIDs that appear inside <system-reminder> blocks.
    text = re.sub(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "<UUID>",
        text,
    )
    # Cache-creation date stamps.
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\b", "<TS>", text)
    # User email — leaked into the # userEmail context block by the
    # subscription account.
    text = re.sub(
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "<USER_EMAIL>", text
    )
    return text


def _normalize_tools(tools: list[dict]) -> list[dict]:
    """Sort tools by name, drop volatile fields."""
    out = []
    for t in tools:
        out.append(
            {
                "name": t.get("name"),
                "description": t.get("description"),
                "input_schema": t.get("input_schema") or t.get("inputSchema"),
                "is_mcp": t.get("is_mcp", False),
                "mcp_server_name": t.get("mcp_server_name"),
            }
        )
    return sorted(out, key=lambda x: x["name"] or "")


_REMINDER_RX = re.compile(r"<system-reminder>(.*?)</system-reminder>", re.DOTALL)


def _walk_text(messages: list[dict]) -> list[str]:
    """Yield the .text of every text block in every message, with real chars."""
    out: list[str] = []
    for m in messages:
        for b in (m.get("content") or []):
            if not isinstance(b, dict):
                continue
            txt = b.get("text") or b.get("content") or b.get("thinking")
            if isinstance(txt, str):
                out.append(txt)
    return out


def _first_user_prompt_text(messages: list[dict]) -> str:
    """Concatenate every text block of the first user message verbatim.

    Claude Code packs skill lists, project context, and other context into
    `<system-reminder>` blocks alongside the actual user prompt. We keep
    them all so user-prompt.md is a faithful record of what claude-code
    actually sent on the user's behalf.
    """
    for m in messages:
        if (m.get("role") or "").lower() != "user":
            continue
        parts: list[str] = []
        for b in (m.get("content") or []):
            if not isinstance(b, dict):
                continue
            txt = b.get("text") or b.get("content")
            if isinstance(txt, str):
                parts.append(txt)
        if parts:
            return "\n\n".join(parts)
    return ""


def _extract_reminders(messages: list[dict]) -> list[str]:
    """Pull every <system-reminder>…</system-reminder> block, with real chars."""
    out: list[str] = []
    for txt in _walk_text(messages):
        out.extend(m.group(1).strip() for m in _REMINDER_RX.finditer(txt))
    return out


_DEFERRED_RX = re.compile(
    r"deferred tools.*?(?:via\s+ToolSearch|ToolSearch).*?:\s*\n(.*?)(?:\n\s*\n|$)",
    re.DOTALL | re.IGNORECASE,
)


_SKILLS_REMINDER_RX = re.compile(
    r"The following skills are available for use with the Skill tool:\s*\n+(.+)",
    re.DOTALL,
)
_SKILL_LINE_RX = re.compile(r"^- ([\w:.\-]+):\s*(.+)$")


def _extract_skills(reminders: list[str]) -> list[dict]:
    """Parse the 'available skills' system-reminder into structured records.

    Each entry is ``{"name": ..., "description": ...}``. The description is
    trimmed to a single line; the full body lives in user-prompt.md.
    """
    out: list[dict] = []
    seen: set[str] = set()
    for rem in reminders:
        m = _SKILLS_REMINDER_RX.search(rem)
        if not m:
            continue
        for line in m.group(1).splitlines():
            sm = _SKILL_LINE_RX.match(line)
            if not sm:
                continue
            name = sm.group(1)
            if name in seen:
                continue
            seen.add(name)
            out.append({"name": name, "description": sm.group(2).strip()})
        break
    return out


def _extract_deferred_tools(reminders: list[str]) -> list[str]:
    """Find tools deferred behind ToolSearch (introduced ~2.1.x).

    Looks for a system-reminder of the form 'The following deferred tools are
    now available via ToolSearch ... :\\n<name>\\n<name>\\n...'.
    """
    names: set[str] = set()
    for r in reminders:
        m = _DEFERRED_RX.search(r)
        if not m:
            continue
        for line in m.group(1).splitlines():
            name = line.strip().rstrip(",")
            if name and " " not in name and name[0].isalpha():
                names.add(name)
    return sorted(names)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: extract.py <results-dir>", file=sys.stderr)
        return 1

    arg = Path(argv[1]).resolve()
    # Local-mode scenarios already have their final artifact (output.txt).
    if arg.is_dir() and (arg / "output.txt").exists() and not (arg / "raw").exists():
        print(f"skipping {arg} (local-mode scenario, output.txt is final)")
        return 0

    capture_arg = arg
    capture_dir = _resolve_capture_dir(capture_arg)

    # Infer <version>/<scenario> from the path:
    # versions/<version>/scenarios/<scenario>/raw/<timestamp>/
    rel = capture_dir.relative_to(REPO_DIR / "versions").parts
    if len(rel) < 5 or rel[1] != "scenarios" or rel[3] != "raw":
        sys.exit(
            f"capture dir not under versions/<dir>/scenarios/<scenario>/raw/<ts>/: {capture_dir}"
        )
    dir_name, scenario = rel[0], rel[2]
    version = version_from_dir(dir_name)

    out_dir = REPO_DIR / "versions" / dir_name / "scenarios" / scenario / "extracted"
    out_dir.mkdir(parents=True, exist_ok=True)

    session = _load_session(capture_dir)
    requests = session.get("requests", [])
    if not requests:
        sys.exit("no requests in session")

    # The first request is often a tools-less haiku side-call (warmup, file
    # path extraction, etc.). The "main" agent request is the first one with
    # tools advertised; fall back to the first request if none have tools.
    first = next((r for r in requests if r.get("tools")), requests[0])
    sys_text = _scrub_volatile(_system_prompt_text(first.get("system_prompt")))
    (out_dir / "system-prompt.md").write_text(sys_text + "\n")

    all_tools = _normalize_tools(first.get("tools", []))
    builtin_tools = [t for t in all_tools if not t.get("is_mcp")]
    mcp_tools_advertised = [t for t in all_tools if t.get("is_mcp")]
    (out_dir / "tools.json").write_text(json.dumps(builtin_tools, indent=2) + "\n")

    # Per-request summary, useful for tracking pipeline shape.
    summary = []
    for i, r in enumerate(requests, start=1):
        summary.append(
            {
                "index": i,
                "model": r.get("model"),
                "duration_ms": r.get("duration_ms"),
                "tool_count": len(r.get("tools", [])),
                "stop_reason": r.get("stop_reason"),
                "input_tokens": (r.get("usage") or {}).get("input_tokens"),
                "output_tokens": (r.get("usage") or {}).get("output_tokens"),
            }
        )
    (out_dir / "requests.json").write_text(json.dumps(summary, indent=2) + "\n")

    # The first user message verbatim — including every <system-reminder>
    # block claude-code injected (skills list, project context, etc.).
    user_prompt = _scrub_volatile(_first_user_prompt_text(first.get("messages", [])))
    (out_dir / "user-prompt.md").write_text(user_prompt + ("\n" if user_prompt else ""))

    # Count reminders for the stats block. Use the first request's user
    # message as the canonical surface; deferred-tool detection still scans
    # the whole conversation since that reminder may arrive after a tool call.
    reminder_count = len(_extract_reminders(first.get("messages", [])))
    all_reminders: list[str] = []
    for r in requests:
        all_reminders.extend(_extract_reminders(r.get("messages", [])))

    deferred_all = _extract_deferred_tools(all_reminders)
    skills = _extract_skills(all_reminders)
    (out_dir / "skills.json").write_text(json.dumps(skills, indent=2) + "\n")
    builtin_deferred = [n for n in deferred_all if not n.startswith("mcp__")]
    mcp_deferred = [n for n in deferred_all if n.startswith("mcp__")]
    (out_dir / "deferred-tools.json").write_text(
        json.dumps(builtin_deferred, indent=2) + "\n"
    )
    # MCP tools are excluded from tools.json / deferred-tools.json so
    # scenario-specific fixtures don't pollute the cross-version diff.
    # Their counts still surface in stats.json for visibility.
    mcp_advertised_count = len(mcp_tools_advertised)
    mcp_deferred_count = len(mcp_deferred)

    # Token totals across the conversation (from agentlens' parsed usage).
    def _u(r, k):
        return (r.get("usage") or {}).get(k) or 0

    in_tokens = sum(_u(r, "input_tokens") for r in requests)
    out_tokens = sum(_u(r, "output_tokens") for r in requests)
    cache_read = sum(_u(r, "cache_read_input_tokens") for r in requests)
    cache_create = sum(_u(r, "cache_creation_input_tokens") for r in requests)
    total_duration = sum((r.get("duration_ms") or 0) for r in requests)

    # Per-scenario stats — aggregated by summarize-version.py into the
    # version-root manifest.json.
    stats = {
        "version": version,
        "dir_name": dir_name,
        "scenario": scenario,
        "captured_at": session.get("session", {}).get("ended_at"),
        "request_count": len(requests),
        "models": sorted({r.get("model") for r in requests if r.get("model")}),
        "tool_count_first_request": len(builtin_tools),
        "deferred_tool_count": len(builtin_deferred),
        "mcp_tool_count_advertised": mcp_advertised_count,
        "mcp_tool_count_deferred": mcp_deferred_count,
        "system_prompt_chars": len(sys_text),
        "user_prompt_chars": len(user_prompt),
        "skill_count": len(skills),
        "reminder_count": reminder_count,
        "tokens": {
            "input": in_tokens,
            "output": out_tokens,
            "cache_read": cache_read,
            "cache_creation": cache_create,
            "total": in_tokens + out_tokens,
        },
        "duration_ms_total": int(total_duration),
    }
    (out_dir / "stats.json").write_text(json.dumps(stats, indent=2) + "\n")

    print(
        f"wrote {out_dir} ({len(requests)} req, {len(builtin_tools)} built-in "
        f"+ {len(builtin_deferred)} deferred, "
        f"{mcp_advertised_count}+{mcp_deferred_count} MCP, "
        f"{len(skills)} skills, {reminder_count} reminders)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
