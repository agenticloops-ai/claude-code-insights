# Scenarios

Each subdirectory is one black-box probe of a `claude-code` version. The
suite is designed so a single capture run yields enough data to track how
the system prompt, tool surface, deferred-tool mechanism, MCP integration,
skill integration, and mode handling change across releases.

## Layout

```
scenarios/<NN>-<name>/
├── prompt.txt        # exact user prompt fed via -p (omitted for local-mode scenarios)
└── meta.json         # how to launch (mode, claude flags, env)
```

`meta.json` schema:

| key | type | purpose |
|---|---|---|
| `name` | string | scenario id (matches dir name) |
| `description` | string | one-paragraph rationale |
| `mode` | `"agent"` \| `"local"` | `agent` (default) runs through agentlens with the API; `local` invokes claude with no proxy and captures stdout (e.g. `claude --help`) |
| `claude_args` | list[string] | extra flags appended before the prompt |
| `env` | object | extra env vars passed to the container |
| `min_version` | string \| absent | semver floor; `run-scenario.sh` exits 125 (skipped, not failed) when the target version is below this. Use for scenarios that exercise a feature introduced in a specific release (e.g. skills shipped in 2.0.28). |

The MCP server is sandbox-permanent: `sandbox/fixtures/mcp-default.json`
defines a single `fixture` server with 3 tools, and `entrypoint.sh` merges
it into `~/.claude.json` on every container start. Claude reads it natively
on startup — no `--mcp-config` flag. There is no per-scenario MCP override;
change the fixture if you need different MCP behavior.

## Running

```bash
# one scenario against one version
scripts/run-scenario.sh 2.1.126 03-bare

# every scenario against one version
scripts/capture-version.sh 2.1.126

# extract version-comparable artifacts for one scenario after capturing
python3 scripts/extract.py versions/2.1.126/scenarios/03-bare

# diff two versions once both are extracted
python3 scripts/diff-versions.py 2.1.59 2.1.126
```

`run-scenario.sh` exit codes: `0` success, `124` per-container timeout (only
when `CAPTURE_TIMEOUT_SECS` is set), `125` skipped (target version below the
scenario's `min_version`), other = failure.

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
- Loads MCP servers from `sandbox/fixtures/mcp-default.json` (single `fixture`
  server, 3 tools), merged into `~/.claude.json` by `entrypoint.sh` on every
  container start. Claude reads them natively, no flag needed. claude.ai
  account-level connectors don't bleed in because the auth volume only holds
  OAuth credentials, not the connector cache. No per-scenario MCP override.
- Always sees the fixture skills under `sandbox/fixtures/skills/` mounted at
  `~/.claude/skills/`.

The wipe makes the *next* scenario start clean. To preserve previous state for
debugging, set `CAPTURE_KEEP_STATE=1` on the docker run env.

## Adding a new scenario

1. Pick the next number, create `scenarios/NN-<name>/`.
2. Drop a `prompt.txt` (skip for local-mode scenarios).
3. Create `meta.json` (copy from a similar scenario).
4. Run it: `scripts/run-scenario.sh <version> NN-<name>`.
5. Extract: `python3 scripts/extract.py versions/<version>/scenarios/NN-<name>`.

## Current set

Ordered so the always-runnable static probe comes first (`01` works on every
version), then the agent-mode probes. Scenarios that depend on a feature
introduced later carry `min_version` and are skipped (not failed) on older
targets. The MCP fixture (server `fixture`, 3 tools) and the skill fixture
(`say-hello`) are sandbox-permanent — `05-with-mcp` and `06-with-skill`
exercise those surfaces explicitly so the diff captures any change in how
claude registers / surfaces them.

| # | name | mode | min_version | what it probes |
|---|---|---|---|---|
| 01 | cli-help | local | — | top-level `claude --help` flag/command surface |
| 03 | bare | agent | — | baseline system prompt, default tools, default model |
| 04 | agent-task | agent | — | multi-turn agent loop (the historical 2.1.59 reference prompt) |
| 05 | with-mcp | agent | — | MCP tool registration & naming convention (probes the always-mounted fixture) |
| 06 | with-skill | agent | 2.0.28 | skill discovery via `<system-reminder>` and the `Skill` tool |
