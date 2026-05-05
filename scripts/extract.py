#!/usr/bin/env python3
"""Extract version-comparable artifacts from an agentlens capture.

Reads versions/<version>/scenarios/<scenario>/raw/<scenario>.json (the
agentlens session export) and writes canonical artifacts to the scenario
root, one level above. The split-out files are designed to diff cleanly
between releases.

Usage:
    scripts/extract.py versions/2026-04-30_2.1.126/scenarios/02-bare
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


def _fixture_skill_names() -> set[str]:
    """Skill directory names mounted by the sandbox — excluded from skills.json so
    cross-version diffs reflect Anthropic-shipped skills only."""
    root = REPO_DIR / "sandbox" / "fixtures" / "skills"
    return {p.name for p in root.iterdir() if p.is_dir()} if root.exists() else set()


def _fixture_mcp_server_names() -> set[str]:
    """MCP server keys from the always-mounted default fixture — excluded from
    MCP tool counts so cross-version diffs reflect non-fixture MCP only."""
    cfg = REPO_DIR / "sandbox" / "fixtures" / "mcp-default.json"
    if not cfg.exists():
        return set()
    try:
        return set((json.loads(cfg.read_text()).get("mcpServers") or {}).keys())
    except Exception:
        return set()


def _load_session(scen_dir: Path) -> dict | None:
    """Load the agentlens session JSON from <scen_dir>/raw/.

    Prefer ``raw/<scenario>.json``; otherwise fall back to the largest JSON
    in raw/ that isn't a per-request split file. Returns None if no usable
    session is present (caller writes a stub stats.json instead of failing).
    """
    raw_dir = scen_dir / "raw"
    if not raw_dir.exists():
        return None
    preferred = raw_dir / f"{scen_dir.name}.json"
    if preferred.exists():
        return json.loads(preferred.read_text())
    candidates = [
        p for p in raw_dir.glob("*.json")
        if not p.name.endswith((".request.json", ".response.json", ".sse.json"))
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_size, reverse=True)
    return json.loads(candidates[0].read_text())


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
    # Strip leaked claude.ai connector / personal-plugin tool names from the
    # deferred-tool listing inside <system-reminder> blocks. Sandbox hardening
    # in entrypoint.sh prevents these going forward, but defending here keeps
    # extracted artifacts clean even if a stale auth volume slips through.
    text = re.sub(
        r"\nmcp__(?:claude_ai|plugin)_?[\w\-]*(?:__[\w\-]*)*", "", text
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


_INJECTED_TAG_RX = re.compile(
    r"<([a-zA-Z][\w\-]*)(?:\s[^>]*)?>.*?</\1>",
    re.DOTALL,
)


def _first_user_prompt_text(messages: list[dict]) -> str:
    """Return only the Claude Code-injected blocks from the first user message.

    Claude Code wraps every piece of context it adds — skill lists, deferred
    tool catalogs, project metadata, command output — in tag blocks like
    ``<system-reminder>…</system-reminder>``, ``<command-name>…</command-name>``,
    ``<local-command-stdout>…</local-command-stdout>``. The user's typed prompt
    is the only naked text. We keep just the tag blocks so user-prompt.md
    diffs reflect changes to claude-code's injection behavior, not changes
    to scenario prompts.
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
            full = "\n\n".join(parts)
            blocks = [m.group(0) for m in _INJECTED_TAG_RX.finditer(full)]
            return "\n\n".join(blocks)
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

# 2.1.69 → 2.1.110-ish era used a top-level <available-deferred-tools> tag in
# the user message (one tool per line) instead of a system-reminder paragraph.
_AVAILABLE_DEFERRED_RX = re.compile(
    r"<available-deferred-tools>\s*(.*?)\s*</available-deferred-tools>",
    re.DOTALL,
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


def _extract_deferred_tools(
    reminders: list[str], extra_text: str = ""
) -> list[str]:
    """Find tools deferred behind ToolSearch (introduced ~2.1.x).

    Two shapes have been observed across releases:
      1. Post-2.1.111-ish: a system-reminder paragraph 'The following deferred
         tools are now available via ToolSearch ...:\\n<name>\\n<name>\\n...'.
      2. ~2.1.69 → 2.1.110: a top-level <available-deferred-tools>…</available-
         deferred-tools> tag in the first user message, one tool per line.

    `reminders` carries shape 1; `extra_text` (typically the first user message)
    carries shape 2.
    """
    names: set[str] = set()

    def _add(line: str) -> None:
        name = line.strip().rstrip(",")
        if name and " " not in name and (name[0].isalpha() or name[0] == "_"):
            names.add(name)

    for r in reminders:
        m = _DEFERRED_RX.search(r)
        if not m:
            continue
        for line in m.group(1).splitlines():
            _add(line)
    if extra_text:
        for m in _AVAILABLE_DEFERRED_RX.finditer(extra_text):
            for line in m.group(1).splitlines():
                _add(line)
    return sorted(names)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: extract.py <results-dir>", file=sys.stderr)
        return 1

    scen_dir = Path(argv[1]).resolve()
    if not scen_dir.is_dir():
        sys.exit(f"scenario dir not found: {scen_dir}")
    # Local-mode scenarios already have their final artifact (output.txt).
    if (scen_dir / "output.txt").exists():
        print(f"skipping {scen_dir} (local-mode scenario, output.txt is final)")
        return 0

    # Infer <version>/<scenario> from the path:
    # versions/<dir-name>/scenarios/<scenario>/
    rel = scen_dir.relative_to(REPO_DIR / "versions").parts
    if len(rel) < 3 or rel[1] != "scenarios":
        sys.exit(
            f"scenario dir not under versions/<dir>/scenarios/<scenario>/: {scen_dir}"
        )
    dir_name, scenario = rel[0], rel[2]
    version = version_from_dir(dir_name)

    out_dir = scen_dir
    session = _load_session(scen_dir)
    requests = (session or {}).get("requests", [])
    if not requests:
        # No session captured (claude CLI errored before agentlens saw a
        # request, or the only request had no body). Write a stub stats.json
        # so /summarize-version can still build the manifest entry.
        stub = {
            "version": version,
            "dir_name": dir_name,
            "scenario": scenario,
            "captured_at": (session or {}).get("session", {}).get("ended_at"),
            "request_count": 0,
            "error": "no requests in session",
        }
        (out_dir / "stats.json").write_text(json.dumps(stub, indent=2) + "\n")
        print(f"wrote stub {out_dir} (0 requests — no session captured)")
        return 0

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

    deferred_all = _extract_deferred_tools(all_reminders, user_prompt)
    fixture_skills = _fixture_skill_names()
    fixture_mcp_servers = _fixture_mcp_server_names()
    skills = [s for s in _extract_skills(all_reminders) if s["name"] not in fixture_skills]
    (out_dir / "skills.json").write_text(json.dumps(skills, indent=2) + "\n")
    builtin_deferred = [n for n in deferred_all if not n.startswith("mcp__")]
    mcp_deferred = [n for n in deferred_all if n.startswith("mcp__")]
    (out_dir / "deferred-tools.json").write_text(
        json.dumps(builtin_deferred, indent=2) + "\n"
    )
    # MCP tools are excluded from tools.json / deferred-tools.json so the
    # always-mounted fixture (server "fixture", 3 tools) doesn't pollute the
    # cross-version tool diff. Counts in stats.json also exclude it for the
    # same reason — the value comparable across versions is "did MCP land in
    # the tool list at all", not "how many fixture tools registered".
    def _is_fixture_mcp(name: str | None) -> bool:
        if not name or not name.startswith("mcp__"):
            return False
        # mcp__<server>__<tool>
        parts = name.split("__", 2)
        return len(parts) >= 2 and parts[1] in fixture_mcp_servers

    mcp_advertised_count = sum(
        1 for t in mcp_tools_advertised if not _is_fixture_mcp(t.get("name"))
    )
    mcp_deferred_count = sum(1 for n in mcp_deferred if not _is_fixture_mcp(n))

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

    # Guardrail: the auth volume previously surfaced the user's claude.ai-attached
    # connectors and personal MCP plugins via the deferred-tools list. Refuse to
    # silently produce polluted artifacts — if anything matching those patterns
    # made it past _scrub_volatile and the is_mcp filter, fail loudly so the
    # operator notices and runs scripts/scrub-leaks.py / re-captures.
    leak_rx = re.compile(r"mcp__(?:claude_ai|plugin)_?[\w\-]*")
    leak_hits: list[str] = []
    for artifact in (
        out_dir / "system-prompt.md",
        out_dir / "user-prompt.md",
        out_dir / "tools.json",
        out_dir / "deferred-tools.json",
        out_dir / "skills.json",
    ):
        if artifact.exists() and leak_rx.search(artifact.read_text()):
            leak_hits.append(artifact.name)
    if leak_hits:
        raise SystemExit(
            f"extract.py: leaked claude.ai/plugin MCP names in {out_dir}: "
            f"{', '.join(leak_hits)}. Re-capture under hardened sandbox or "
            f"run scripts/scrub-leaks.py."
        )

    print(
        f"wrote {out_dir} ({len(requests)} req, {len(builtin_tools)} built-in "
        f"+ {len(builtin_deferred)} deferred, "
        f"{mcp_advertised_count}+{mcp_deferred_count} MCP, "
        f"{len(skills)} skills, {reminder_count} reminders)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
