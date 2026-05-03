# Scenarios

Each subdirectory is one black-box probe of a `claude-code` version. The
suite is designed so a single capture run yields enough data to track how
the system prompt, tool surface, deferred-tool mechanism, MCP integration,
skill integration, and mode handling change across releases.

## Layout

```
scenarios/<NN>-<name>/
├── prompt.txt        # exact user prompt fed via -p (omitted for local-mode scenarios)
├── meta.json         # how to launch (mode, claude flags, mcp, env)
└── mcp.json          # only if the scenario advertises an MCP server
```

`meta.json` schema:

| key | type | purpose |
|---|---|---|
| `name` | string | scenario id (matches dir name) |
| `description` | string | one-paragraph rationale |
| `mode` | `"agent"` \| `"local"` | `agent` (default) runs through agentlens with the API; `local` invokes claude with no proxy and captures stdout (e.g. `claude --help`) |
| `claude_args` | list[string] | extra flags appended before the prompt |
| `mcp` | string \| null | path to mcp.json (relative to repo root); merged into the default fixture |
| `env` | object | extra env vars passed to the container |

## Running

```bash
# one scenario against one version
scripts/run-scenario.sh 2.1.126 03-with-mcp-3tools

# every scenario against one version
scripts/capture-version.sh 2.1.126

# extract version-comparable artifacts for one scenario after capturing
python3 scripts/extract.py versions/2.1.126/scenarios/03-with-mcp-3tools

# diff two versions once both are extracted
python3 scripts/diff-versions.py 2.1.59 2.1.126
```

Or use the `/process-version` skill to run all of the above end-to-end:

```bash
claude -p "/process-version 2.1.126 --diff-from 2.1.59"
```

## Isolation guarantees

Every scenario:

- Runs in a fresh single-use container (`docker run --rm`)
- Sees a `cch-auth` Docker volume that has its **transient state wiped** at
  entrypoint (transcripts, plans, sessions, todos, plugins, agentlens DB).
  Only `.claude.json`, `.claude/.credentials.json`, `.claude/settings.json`,
  and `.mitmproxy/` survive.
- Loads MCP servers from a single merged JSON: `sandbox/fixtures/mcp-default.json`
  plus the scenario's `mcp.json` (if any). `--strict-mcp-config` is always set
  so claude.ai connectors never bleed in.
- Always sees the fixture skills under `sandbox/fixtures/skills/` mounted at
  `~/.claude/skills/`.

The wipe makes the *next* scenario start clean. To preserve previous state for
debugging, set `CAPTURE_KEEP_STATE=1` on the docker run env.

## Adding a new scenario

1. Pick the next number, create `scenarios/NN-<name>/`.
2. Drop a `prompt.txt` (skip for local-mode scenarios).
3. Create `meta.json` (copy from a similar scenario).
4. If the scenario needs its own MCP server, add `mcp.json` with `command`/`args`
   pointing at `/opt/fixtures/mcp/...` (mounted at runtime) or any binary on
   `$PATH` inside the container.
5. Run it: `scripts/run-scenario.sh <version> NN-<name>`.
6. Extract: `python3 scripts/extract.py versions/<version>/scenarios/NN-<name>`.

## Current set

| # | name | mode | what it probes |
|---|---|---|---|
| 01 | bare | agent | baseline system prompt, default tools, default model |
| 02 | agent-task | agent | multi-turn agent loop (the historical 2.1.59 reference prompt) |
| 03 | with-mcp-3tools | agent | MCP tool registration & naming convention |
| 04 | with-skill | agent | skill discovery via `<system-reminder>` |
| 05 | many-tools-30 | agent | ToolSearch / deferred-tools threshold |
| 06 | plan-mode | agent | `--permission-mode plan` reminder injection |
| 07 | cli-help | local | top-level `claude --help` flag/command surface |
| 08 | websearch | agent | how the agent picks and calls a web-search tool unaided |
