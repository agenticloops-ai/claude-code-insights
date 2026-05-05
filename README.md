<div align="center">

# 🔬 Claude Code Evolution

**The changelog Anthropic doesn't publish.**\
Black-box capture and diff of [`@anthropic-ai/claude-code`](https://www.npmjs.com/package/@anthropic-ai/claude-code) across releases — system prompt, tool catalog, deferred-tool registry, skills, and `<system-reminder>` injections, version by version.

*by [AgenticLoops.ai](https://agenticloops.ai) — for engineers, from engineers*

[![Website](https://img.shields.io/badge/Website-agenticloops.ai-green?style=for-the-badge&logo=googlechrome&logoColor=white)](https://agenticloops.ai)
[![Substack](https://img.shields.io/badge/Substack-Blogs_&_Newsletter-orange?style=for-the-badge&logo=substack&logoColor=white)](https://agenticloopsai.substack.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/agenticloops-ai)
[![Follow @agenticloops_ai](https://img.shields.io/badge/Follow%20%40agenticloops__ai-black?style=for-the-badge&logo=x&logoColor=white)](https://x.com/agenticloops_ai)

</div>

> **You don't need the leaked source code to understand Claude Code.** The interesting part isn't the TypeScript — it's the **prompts and the tool use**. Both travel over the wire on every single request, in plaintext, on their way to `api.anthropic.com`. Pin a version, capture the traffic, diff against the next version. That's the changelog Anthropic doesn't publish.
>
> If the *why* of "prompts and tool use are the whole game" doesn't click yet, read [**How agents work — the patterns behind**](https://open.substack.com/pub/agenticloopsai/p/how-agents-work-the-patterns-behind?r=1lm8w&utm_medium=ios) first. Then come back here for the receipts, version by version.

## 🔍 What's Inside

For each pinned version, this repo contains the parts of Claude Code that travel on the wire — captured through an MITM proxy under a controlled Docker sandbox, scrubbed of volatile fingerprints, and committed as plain text so the diff between any two releases is one `git diff` away.

**For each captured version you'll find:**

- **System Prompt** — the exact instructions Claude Code feeds the model on every request
- **Tool Catalog** — every advertised tool with its full JSON schema, sorted and normalized
- **Deferred Tools** — names hidden behind `ToolSearch` (the lazy-loading mechanism that landed in 2.1.x)
- **Skills** — the `{name, description}` pairs surfaced in the "available skills" reminder
- **`<system-reminder>` blocks** — every piece of context Claude Code injects into your first user message
- **Per-scenario stats** — request count, model routing, token totals, durations, stop reasons
- **Version-to-version diff** — markdown report covering tools added/removed/moved-to-deferred, skill changes, system-prompt unified diff, CLI flag deltas

> **Things you can already discover by reading the diffs:**
>
> 🤖 [**The default model swapped four times in twelve months**](versions/) — sonnet-3-7 → opus-4 → opus-4-1 → sonnet-4-5 → opus-4-7. Every release walks the metric table.\
> 🪄 [**`ToolSearch` and the deferred-tools mechanism appeared in 2.1.x**](versions/2026-04-30_2.1.126/diff-from-2025-09-29_2.0.0.md#tools) — `WebFetch`, `WebSearch`, `NotebookEdit`, `TodoWrite`, `ExitPlanMode` all moved from advertised to deferred between 2.0.0 and 2.1.126.\
> 📈 [**The system prompt more than doubled at 2.1**](versions/2026-04-30_2.1.126/diff-from-2025-09-29_2.0.0.md) — 12339 → 26719 chars. Most of the new bytes are tone, planning, and "executing actions with care" sections.\
> 🛠️ [**16 new top-level tools at 2.1**](versions/2026-04-30_2.1.126/diff-from-2025-09-29_2.0.0.md#tools) — `Agent`, `AskUserQuestion`, `CronCreate`, `EnterPlanMode`, `Skill`, `ToolSearch`, `ScheduleWakeup`, `Monitor`, `RemoteTrigger`, `PushNotification`, and more. Built-in skills jumped from zero to ten.

**Useful for:**

- **Engineers pinning Claude Code in production** — see what's about to change in the prompt that drives every response *before* you upgrade.
- **Prompt and tool-use authors** — Anthropic ships some of the best-tuned agent prompts in production. The diffs are a free apprenticeship in how a real shop iterates on tool descriptions, reminder phrasing, deferred-tool thresholds, and model routing.
- **Researchers** studying how agent surfaces evolve under real release pressure.
- **Anyone curious** about what *actually* changed when `claude --help` started listing a flag yesterday that wasn't there last week.

---

## 🗺️ Start Here

New to the repo? Follow this reading path:

1. **Pick two versions** — `ls versions/` lists the captured set. Folder names are `<release-date>_<version>` so they sort chronologically.
2. **Open the newer version's `diff-from-<earlier>.md`** — start with the metric table at the top, then scan the section headers (`## tools`, `## skills`, `## system prompt`, …).
3. **Drill into the unified diffs** — `## system prompt` and `## user prompt (incl. system-reminder blocks)` are where the prose-level changes live.
4. **Compare the full extracted artifacts** — `versions/<v>/system-prompt.md`, `tools.json`, `skills.json`, `deferred-tools.json` are what every session sees regardless of how `claude` is invoked.
5. **Dig into a scenario** — `versions/<v>/scenarios/<NN>-<name>/` holds the per-probe extraction (multi-turn agent loop, MCP/skill probes, …) and the raw agentlens capture under `raw/`.

---

## 🧭 Tracing changes across versions

The repo is organized as a chain of captured snapshots; each newer version carries a diff against the previous one. The fastest way to read the history is to walk the diff chain in `versions/`. [`VERSIONS.md`](VERSIONS.md) (regenerated by `/refresh-versions`) is the full npm release index and marks which versions are captured.

### How to read a single version

Open `versions/<release-date>_<version>/` and you'll find:

```
versions/<release-date>_<version>/
├── stats.md                # at-a-glance per-scenario summary table
├── manifest.json           # aggregate counts (tools, skills, tokens, durations)
├── system-prompt.md        # baseline scenario's system prompt (volatile bits scrubbed)
├── user-prompt.md          # baseline first user message — only the claude-code-injected blocks
├── tools.json              # built-in tool list (sorted, normalized)
├── deferred-tools.json     # tools hidden behind ToolSearch
├── skills.json             # skills surfaced in the "available skills" reminder
├── release-notes.md        # upstream CHANGELOG.md entry (or "no entry")
├── diff-from-<earlier>.md  # markdown diff vs the previous captured version
└── scenarios/<NN>-<name>/
    ├── system-prompt.md    # this scenario's extracted artifacts
    ├── user-prompt.md      #   (mirror the version-root files for the baseline)
    ├── tools.json
    ├── deferred-tools.json
    ├── skills.json
    ├── requests.json       # per-request summary (model, duration, tokens, stop reason)
    ├── stats.json          # this scenario's aggregate counts
    └── raw/                # everything agentlens captured, kept verbatim
        ├── agentlens.log
        ├── <scenario>.json   # full session export
        ├── <scenario>.md
        ├── <scenario>.csv
        ├── 001.request.json  # per-request raw (split-raw.py output)
        ├── 001.response.json
        └── 001.sse.json
```

The version-root files are the **baseline** scenario's extracted artifacts (`02-bare`, single-turn `hi`, with the always-mounted MCP fixture and skill fixture) promoted up. They're what every session sees regardless of how you invoke `claude`. Per-scenario folders dig into anything specific (multi-turn agent loop, MCP/skill probes).

### How to read a diff

`diff-from-<earlier>.md` follows a fixed template so each version's delta is comparable:

1. **Metric table** — net change in tool count, deferred-tool count, system-prompt size, reminder count, model.
2. **`## tools`** — tools added / removed / moved-to-deferred / moved-to-advertised / new-deferred / modified.
3. **`## skills`** — skills added / removed / description-changed.
4. **`## system prompt`** — unified diff of the system prompt.
5. **`## user prompt (incl. system-reminder blocks)`** — unified diff of the injected user-message context.
6. **`## cli: 01-cli-help`** — added/removed CLI flags & commands, with the full `claude --help` diff in a `<details>` block.

If a section is missing, nothing changed at that surface in this release.

### Asking "what changed about X"

| question | where to look |
|---|---|
| Did the default model change? | `manifest.json → baseline.models`, or the metric table at the top of the diff |
| Was a tool renamed / moved behind `ToolSearch`? | `## tools` in the diff (`moved_to_deferred`, `moved_to_advertised`) |
| Did a tool description change? | `## tools → modified` in the diff; full text in `tools.json` |
| Did a built-in skill appear or change wording? | `## skills` in the diff; full descriptions in `skills.json` |
| Did the system prompt grow / shrink / reorder? | metric table (`system_prompt_chars`) + `## system prompt` |
| Did claude-code start injecting a new `<system-reminder>`? | `## user prompt (incl. system-reminder blocks)` |
| Did a new CLI flag ship? | `## cli: 01-cli-help` |
| How does scenario X behave on this version? | `versions/<v>/scenarios/<NN>-<name>/stats.json` and `requests.json` |

---

## 🔬 Research approach

All artifacts in this repo were captured using [**AgentLens**](https://github.com/agenticloops-ai/agentlens), an open-source MITM proxy that intercepts LLM API traffic during normal agent use, plus a thin Docker sandbox that pins one Claude Code version per image so captures are byte-comparable across hosts and months.

**How it works:**

1. **Pin** — `sandbox/Dockerfile` builds an image with one fixed `@anthropic-ai/claude-code` version plus `agentlens-proxy` and a deterministic fixture set (one demo MCP server, one fixture skill, a stripped settings file). No host `~/.claude`, no host MCP, no host git.
2. **Capture** — `scripts/capture-version.sh <version>` runs every scenario in a fresh container. AgentLens transparently records every request and response (system prompt, tool definitions, messages, token usage, timing) to `versions/<v>/scenarios/<s>/raw/`.
3. **Extract** — `scripts/extract.py` reads the agentlens session JSON and writes the version-comparable artifacts (`system-prompt.md`, `tools.json`, `deferred-tools.json`, `skills.json`, `requests.json`, `stats.json`) to the scenario root. Volatile fingerprints (UUIDs, timestamps, cache-busters, the user email) are scrubbed so artifacts diff cleanly across runs.
4. **Diff** — `scripts/diff-versions.py <from> <to>` produces the markdown report at `versions/<to>/diff-from-<from>.md`.

The whole pipeline is driven by a single slash command: `/process-version <version> [--diff-from <previous-version>]`.

---

## 💡 Key insights so far

These are patterns that jumped out while walking the diff chain `0.2.126 → 1.0.0 → 1.0.128 → 2.0.0 → 2.1.126`. Open the linked diff to see the receipts.

1. **Tool count is *not* a useful signal on its own.** From 1.0.128 → 2.0.0 the advertised tool count dropped by one (16 → 15) and the system prompt shrank (13878 → 12339 chars). That looks like a simplification. From 2.0.0 → 2.1.126 the advertised tool count *also* dropped (15 → 10) — but it shipped with **17 new deferred tools** behind `ToolSearch`, **16 net-new top-level tools**, and a **system prompt that more than doubled** (12339 → 26719 chars). The metric table is the only honest at-a-glance summary.

2. **`ToolSearch` is the architectural shift of 2.1.** Before 2.1, every tool was advertised on every request — a flat namespace. 2.1 introduced lazy-loaded "deferred" tools fetched on demand. `WebFetch`, `WebSearch`, `NotebookEdit`, `TodoWrite`, and `ExitPlanMode` were silently moved off the advertised list. The same release added 12 new tools that exist *only* in the deferred set (`AskUserQuestion`, `CronCreate`, `Monitor`, `RemoteTrigger`, …). If you're targeting Claude Code's tool surface in production, the deferred set is real and you cannot tell from a single request which tools the model can reach.

3. **Behavior is shaped by injection, not just by the system prompt.** The system prompt is identical across plan and agent modes. Plan mode is enforced by a `<system-reminder>` block in the *first user message* — runtime-injected, scenario-specific. The reminder count metric in each diff (0 → 1 → 1 → 1 → 3) tracks how aggressively claude-code packs the user turn with context.

4. **Built-in skills appeared from nothing in 2.1.** Versions 0.x → 2.0 surface zero skills in the discovery reminder. 2.1 ships with ten: `claude-api`, `simplify`, `update-config`, `keybindings-help`, `init`, `loop`, `review`, `schedule`, `security-review`, `fewer-permission-prompts`. Skills are a parallel surface to tools — discoverable through a separate `<system-reminder>` and invoked through the new `Skill` tool.

5. **The CLI surface grew faster than the agent surface.** The `claude --help` flag list expanded by ~24 flags between 2.0.0 and 2.1.126 (`--agent`, `--auto-mode`, `--effort`, `--betas`, `--from-pr`, `--max-budget-usd`, `--ultrareview`, …) and added six new subcommands. Lots of the new product surface lives on the CLI side, not the model side.

6. **Anthropic ships a haiku side-call pipeline.** Across every version, the baseline scenario shows a small Haiku model (`claude-3-5-haiku-*` → `claude-haiku-4-5-*`) running alongside the main Opus/Sonnet model. Per-scenario `requests.json` shows it's used as a warm-up / file-path-extraction step, not titling. Anthropic's own agent uses a multi-model pipeline.

These will get fleshed out version-by-version once `/process-version` is re-run end-to-end across the whole captured set. For now, follow the diff links above for the unmodified evidence.

---

## 📂 Repository layout

```
.
├── scenarios/             # one black-box probe per directory (prompt + meta)
├── sandbox/               # Docker image + entrypoint + run.sh + fixtures (mcp, skills, settings)
├── scripts/               # capture / extract / summarize / diff / release-notes / refresh-versions
├── .claude/skills/        # /process-version, /extract-capture, /diff-versions
├── versions/              # captured artifacts, one folder per version
└── VERSIONS.md            # generated index of every npm release, regenerated by /refresh-versions
```

### Scenarios

Five probes, ordered so the always-runnable static probe comes first (`01` works on every version) and the agent-mode probes follow. The MCP fixture (server `fixture`, 3 tools) and the skill fixture (`say-hello`) are sandbox-permanent, but `03-with-mcp` and `04-with-skill` exercise those surfaces explicitly so the diff captures any change in how claude registers and surfaces them. Scenarios that exercise a feature introduced later carry a `min_version` and are skipped (not failed) on older releases:

| # | name | mode | min_version | what it probes |
|---|---|---|---|---|
| 01 | cli-help | local | — | top-level `claude --help` flag/command surface |
| 03 | bare | agent | — | baseline system prompt, default tools, default model |
| 04 | agent-task | agent | — | multi-turn loop with Write/Read/Bash + any haiku side-call pipeline |
| 05 | with-mcp | agent | — | MCP tool registration & naming convention (probes the always-mounted fixture) |
| 06 | with-skill | agent | 2.0.28 | skill discovery via `<system-reminder>` and the `Skill` tool |

`02-bare` is the **baseline** — its extracted artifacts are mirrored to the version root. Every other scenario adds one isolated probe surface on top. See `scenarios/README.md` for the full `meta.json` schema and isolation guarantees.

---

## 🚀 Quick start

Once-per-host setup (any version works to populate the `cch-auth` Docker volume):

```bash
./sandbox/login.sh <version>
```

Capture + extract + summarize + release-notes + diff for one version:

```bash
claude -p "/process-version <version> --diff-from <previous-version>"
```

Or call the primitives directly:

```bash
scripts/capture-version.sh <version>                         # all scenarios
scripts/run-scenario.sh    <version> <scenario>              # one scenario
python3 scripts/extract.py            versions/<dir>/scenarios/<scenario>
python3 scripts/summarize-version.py  <version>
python3 scripts/fetch-release-notes.py <version>
python3 scripts/diff-versions.py      <from-version> <to-version>
```

Refresh the version index:

```bash
claude /refresh-versions       # or: python3 scripts/refresh-versions.py
```

### Skills

Three slash commands live in `.claude/skills/`. They're how the pipeline is meant to be driven — the LLM owns orchestration, the bash/Python scripts under `scripts/` are thin primitives the skills call via the Bash tool.

**`/process-version <version> [--diff-from <previous-version>]`** — end-to-end orchestrator. Runs every scenario through the sandbox, extracts each capture, promotes the baseline to the version root, fetches the upstream release notes, and (optionally) writes a diff against a prior version. Idempotent.

**`/extract-capture <scenario-dir>`** — turn one raw agentlens capture (`scenarios/<NN>/raw/`) into the version-comparable artifacts at the scenario root. Used internally by `/process-version`.

**`/diff-versions <from-version> <to-version>`** — generate a markdown diff between **any two captured versions**. Output lands at `versions/<to-dir>/diff-from-<from-dir>.md`. Either argument can be the npm version (`2.1.126`) or the dated folder name (`2026-04-30_2.1.126`).

---

## 🛡️ Sandbox isolation

- Every scenario runs in a fresh `docker run --rm` container; the `cch-auth` Docker volume is wiped of transient state at entrypoint (only OAuth credentials and the mitmproxy CA survive).
- The MCP server is sandbox-permanent: `sandbox/fixtures/mcp-default.json` (single `fixture` server, 3 tools) is merged into `~/.claude.json` by `entrypoint.sh` on every container start. claude reads it natively, no `--mcp-config` flag. claude.ai account-level connectors don't bleed in because the auth volume only holds OAuth credentials.
- The fixture skill set under `sandbox/fixtures/skills/` is bind-mounted at `~/.claude/skills/` so skill discovery is deterministic.
- For older claude versions that lack `--strict-mcp-config`, `sandbox/run.sh` probes `claude --help` and conditionally drops unsupported flags.

See `sandbox/README.md` for the auth model, layout, and what gets pinned in the image.

---

## 🗺️ Coverage strategy

The captured set under `versions/` currently spans the lowest and highest published version of each major (`0.x`, `1.x`, `2.x`). Some scenarios fail on older versions because they exercise flags or models introduced later (`--permission-mode plan`, `--allowed-tools`, retired models, etc.) — those failures are visible per-scenario in the version's `manifest.json` and are expected.

Once the scenario set is finalized, `/process-version` will be re-run across every captured version so the chain of `diff-from-*.md` files reflects the same probes end-to-end.

## 📋 Requirements

- Docker Desktop / Docker Engine
- Python 3 on the host (used for MCP-config merging and the helper scripts)
- A Claude subscription (logged in once via `sandbox/login.sh`)

---

## ⚠️ Disclaimer

This repository is for **educational and research purposes only**. All trademarks belong to their respective owners. The goal is to understand and learn from this system, not to replicate it.

## 📜 Legal notice

This analysis was conducted through observation of network traffic during normal use of publicly available software. No security measures were bypassed, no proprietary source code was accessed, and no terms of service were violated beyond what is necessary for standard interoperability research. Captures are run inside an isolated Docker sandbox using a Claude subscription account; no other user's data is involved.

This is independent research and is not affiliated with, endorsed by, or connected to Anthropic.

## ⚖️ License

MIT
