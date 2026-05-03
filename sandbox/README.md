# Sandbox

Self-contained Docker environment for capturing Claude Code CLI behavior across releases.

## Goal

Run a pinned version of `claude` in an isolated container so the captured
system prompt, tool list, and reminders are byte-comparable across runs and
across host machines. Both `claude` and AgentLens (the MITM proxy that records
the traffic) live inside the image — the only host dependency is Docker.

No real `~/.claude`, no real git repo, no host MCP servers, no host skills,
no host AgentLens — only what we explicitly mount in. Auth uses your Claude
subscription via OAuth, stored in a dedicated Docker volume.

## Layout

```
sandbox/
├── Dockerfile            # node:20 + pinned claude-code + pinned agentlens-proxy
├── entrypoint.sh         # boots agentlens, sets HTTP_PROXY, exec's the agent
├── build.sh              # docker build cch:<version> if missing
├── login.sh              # one-time interactive OAuth into the cch-auth volume
├── run.sh                # docker run a single capture scenario
└── fixtures/
    ├── home/.claude/settings.json   # mounted readonly into the runner home
    ├── workdir/                      # mounted readonly as cwd (no git)
    ├── mcp-default.json              # base MCP config merged into every scenario
    ├── mcp/fixture-mcp.py            # synthetic stdio MCP server (configurable tool count)
    └── skills/say-hello/             # fixture skill mounted at ~/.claude/skills/
```

`fixtures/` is read-only inside the container so a misbehaving session can't
mutate it between runs.

## Prerequisites

- Docker Desktop (or Docker Engine)
- Python 3 on the host (used by `run.sh` to merge MCP configs before launch)
- A Claude subscription account (logged in once via `sandbox/login.sh`)

## Usage

```bash
# 1. one-time OAuth login (creates the cch-auth volume)
./sandbox/login.sh 2.1.126

# 2. run a capture scenario (defaults to versions/<version>/scenarios/<session>/)
./sandbox/run.sh 2.1.126 -- -p "hi"

# 3. or with custom paths
./sandbox/run.sh 2.1.126 -o versions/2.1.126/scenarios/01-bare/raw -s 01-bare -- -p "hi"
```

The first invocation for a given version builds the image (`cch:<version>`);
subsequent runs reuse it. Inside the container, `agentlens wait` runs in the
background, captures all `api.anthropic.com` traffic, and exports JSON +
markdown + CSV to `/results` (mounted to your chosen host path) when the
agent exits.

## Auth model

OAuth credentials live in a named Docker volume `cch-auth` mounted at
`/home/runner` inside the container. This means:

- Login once, reuse across every Claude Code version you build
- Credentials never touch your host filesystem
- `docker volume rm cch-auth` to wipe and re-login

Our fixture `settings.json` is layered on top of the volume as a readonly
bind mount, so each run gets a deterministic settings file regardless of
what the previous session may have written.

## MCP isolation and the merged-config trick

Subscription auth pulls in every connector you've enabled at
`claude.ai/settings/connectors` (Canva, Figma, Gmail, etc.) — these are
account-scoped, not file-scoped, so a clean home directory is not enough.

`run.sh` always passes `--strict-mcp-config` plus a single merged MCP file
that combines `fixtures/mcp-default.json` (the demo server) with the
scenario's optional `--mcp <path>` config. Result:

- Account-level claude.ai connectors are **always** ignored.
- The demo server (1 tool) appears in **every** scenario, so the baseline
  shows how MCP gets registered.
- Scenarios that pass `--mcp` **add** servers on top — they don't replace
  the demo server.

Why merge instead of repeating the flag: `claude --mcp-config <configs...>`
is variadic and uses last-wins replacement when given twice. Passing the
default and the scenario file as two flags would silently drop the default.

## What gets pinned

- `@anthropic-ai/claude-code@<CLAUDE_VERSION>` (build arg, required)
- `agentlens-proxy==<AGENTLENS_VERSION>` (build arg, optional — latest if unset)
- `node:20-bookworm-slim` base
- `LANG=C.UTF-8`, `TZ=UTC`, `--hostname sandbox`, uid/gid 1000
- Empty `cwd` (no git, no skills, no MCP — except via fixtures)

## Output

```
versions/<version>/scenarios/<scenario>/
├── system-prompt.md      # extract.py outputs at the scenario root
├── user-prompt.md
├── tools.json
├── deferred-tools.json
├── skills.json
├── requests.json
├── stats.json
└── raw/                  # everything captured by agentlens
    ├── agentlens.log
    ├── <scenario>.json   # full captured traffic
    ├── <scenario>.md
    ├── <scenario>.csv
    ├── 001.request.json  # per-request raw (split-raw.py)
    ├── 001.response.json
    └── 001.sse.json
```

`run-scenario.sh` lifts agentlens' timestamped subdirectory up to `raw/`
after each capture, so the layout above is what you see on disk regardless
of when the run happened. `scripts/extract.py` reads `raw/<scenario>.json`
and writes the version-comparable artifacts to the scenario root.
