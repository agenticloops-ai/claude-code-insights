---
name: extract-capture
description: Process raw agentlens captures under versions/<v>/scenarios/<s>/raw/ and write version-comparable artifacts into versions/<v>/scenarios/<s>/extracted/. Accepts either a single scenario path or a whole version (loops every scenario). Use whenever new sandbox captures have landed and you need the diff-friendly extracted form.
---

# extract-capture

The sandbox writes raw agentlens output to `versions/<v>/scenarios/<s>/raw/<timestamp>/<scenario>.json`. To track changes across releases we extract a small canonical set of files into `versions/<v>/scenarios/<s>/extracted/`. This skill drives `scripts/extract.py` for one scenario or for every scenario in a version.

## When to invoke

- A new capture just landed under `versions/<v>/scenarios/<s>/raw/`.
- The user asks to "extract", "process the capture", "snapshot this version".
- Called by the `/process-version` orchestrator after `capture-version.sh` finishes.

## How to run

**Single scenario** — pass the scenario directory:
```bash
python3 scripts/extract.py versions/<version>/scenarios/<scenario>
```
The script auto-resolves the most recent timestamp under `raw/`. Local-mode scenarios (those with `output.txt` and no `raw/`, e.g. `07-cli-help`, `09-mcp-help`) are detected and skipped — their captured stdout is already the final artifact.

**Whole version** — loop every scenario:
```bash
for d in versions/<version>/scenarios/*/; do
    python3 scripts/extract.py "$d"
done
```

Report which scenarios were extracted, which were skipped (local mode), and which failed (non-zero exit). Don't dump the resulting files; just confirm counts.

## What the extractor produces (per scenario)

Written to `versions/<v>/scenarios/<s>/extracted/`:

| file | content |
|---|---|
| `system-prompt.md` | system prompt of the first request, with volatile fingerprints scrubbed |
| `user-prompt.md` | first user message verbatim, including all `<system-reminder>` blocks |
| `tools.json` | normalized + sorted built-in tool list (MCP tools excluded; counted in `stats.json`) |
| `deferred-tools.json` | built-in tool names hidden behind `ToolSearch` |
| `skills.json` | `{name, description}` pairs parsed from the "available skills" reminder |
| `requests.json` | per-request summary (model, duration, tokens, stop reason) |
| `stats.json` | aggregate counts: tool/skill/reminder/MCP counts, token totals, durations |

## Notes

- The script scrubs cache fingerprints (`cch=…`), UUIDs, ISO timestamps, and the user email so artifacts are safe to commit.
- If multiple timestamp subdirs exist under `raw/`, the most recent one wins. Pass the full path (e.g. `versions/<v>/scenarios/<s>/raw/<ts>`) to pin a specific capture.
- Do not modify `scripts/extract.py` when the user just wants extraction; only edit it if they want to change *what* is extracted.
- Built-in vs MCP separation is intentional — `tools.json` and `deferred-tools.json` exclude MCP tools so cross-version diffs aren't polluted by per-scenario fixtures. MCP counts still surface in `stats.json`.
