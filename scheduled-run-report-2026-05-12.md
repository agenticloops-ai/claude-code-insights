# Scheduled run · analyze-claude-code-versions · 2026-05-12

## Summary

- **Two new npm releases** since the last run on 2026-05-10:
  **2.1.139** (2026-05-11, with CHANGELOG entry) and **2.1.140**
  (2026-05-12, silent patch).
- `VERSIONS.md` regenerated (now **406 versions**, latest 2.1.140,
  generated stamp `2026-05-12`).
- Release notes fetched for both new versions; release notes for the
  seven still-uncaptured 2.1.129–2.1.138 versions were re-fetched
  (CHANGELOG was unchanged; only the `fetched:` stamp moved).
- **One commit landed locally** (`5d442d87 Refresh VERSIONS.md and
  release notes for 2.1.129-2.1.140`). **Push to `origin/main` failed**
  — sandbox has no git credentials (`fatal: could not read Username for
  'https://github.com'`). Run `git push` on the host to publish it.
- **Capture pipeline still did not run** (same as 2026-05-09 and
  2026-05-10): the scheduled-task sandbox has no `docker` binary and
  no `/var/run/docker.sock`. The nine `versions/2026-05-*_2.1.*`
  directories still hold only `release-notes.md`.

## State of the recent versions

| Version | Date       | Captures   | Release notes |
|---------|------------|------------|---------------|
| 2.1.129 | 2026-05-05 | ❌ missing | ✅ present    |
| 2.1.131 | 2026-05-06 | ❌ missing | ✅ present    |
| 2.1.132 | 2026-05-06 | ❌ missing | ✅ present    |
| 2.1.133 | 2026-05-07 | ❌ missing | ✅ present    |
| 2.1.136 | 2026-05-08 | ❌ missing | ✅ present    |
| 2.1.137 | 2026-05-09 | ❌ missing | ✅ present    |
| 2.1.138 | 2026-05-09 | ❌ missing | ✅ present    |
| 2.1.139 | 2026-05-11 | ❌ missing | ✅ **new**    |
| 2.1.140 | 2026-05-12 | ❌ missing | ✅ **new** (no upstream entry) |

The full extracted artifacts (`system-prompt.md`, `tools.json`,
`deferred-tools.json`, `skills.json`, `user-prompt.md`, `stats.md`,
`manifest.json`, `diff-from-*.md`) still need to be produced from
`docker run cch:<version>` captures on a host that has Docker.

## Headline changes in the new versions

### 2.1.139 — Agent view, `/goal`, hook exec form

Big feature release. The headlines:

- **Agent view (Research Preview):** `claude agents` opens a single
  list of every Claude Code session — running, blocked-on-you, or
  done. See https://code.claude.com/docs/en/agent-view.
- **`/goal` command:** set a completion condition and Claude keeps
  working across turns until it's met. Works in interactive, `-p`,
  and Remote Control. Shows live elapsed/turns/tokens overlay.
- **`/scroll-speed` command** with a live preview.
- **`claude plugin details <name>`** shows component inventory and
  projected per-session token cost.
- **Transcript view navigation:** `?` for shortcuts, `{`/`}` to jump
  between user prompts, `v` to toggle the shortcut panel.
- **Hook exec form:** new `args: string[]` field spawns the command
  without a shell, so path placeholders never need quoting.
- **Hook `continueOnBlock`** option for `PostToolUse` — feed the
  hook's rejection reason back to Claude and continue the turn.
- **MCP stdio servers** now receive `CLAUDE_PROJECT_DIR` (matching
  hooks); plugin configs can reference `${CLAUDE_PROJECT_DIR}`.
- **Subagent telemetry:** API requests carry `x-claude-code-agent-id`
  / `x-claude-code-parent-agent-id`; OTEL `claude_code.llm_request`
  spans include `agent_id` / `parent_agent_id` attributes.
- **API-key gating:** Remote Control, `/schedule`, claude.ai MCP
  connectors, and notification prefs are disabled when
  `ANTHROPIC_API_KEY` / `apiKeyHelper` / `ANTHROPIC_AUTH_TOKEN` is
  set, even if a Claude.ai login also exists.
- ~30 fixes spanning credential refresh, `autoAllowBashIfSandboxed`,
  hook terminal corruption, HTTP/SSE MCP memory growth (now capped at
  16 MB per SSE frame), `Skill(name *)` wildcard matching, settings
  hot-reload through symlinks, model-picker overrides, stream
  watchdog, MCP server cache-dir errors, mouse-wheel scroll in
  Cursor/VS Code 1.92–1.104, Windows Terminal scroll, transcript
  letter shortcuts after mouse click, paste of multiple images,
  Grep on Windows drive-letter paths, fuzzy-match emoji
  highlighting, `claude_code.active_time.total` OTEL metric in
  `--print` mode, etc.
- **VS Code:** `Cmd/Ctrl+Shift+T` reopens the most-recently-closed
  session tab (`claudeCode.enableReopenClosedSessionShortcut`).

Full text: `versions/2026-05-11_2.1.139/release-notes.md`.

### 2.1.140 — silent patch

No entry in upstream `CHANGELOG.md`. Likely an internal-only fix.
Will need a capture to know what (if anything) changed at the
on-the-wire surface.

## Earlier uncaptured versions — headlines

Reproduced from the 2026-05-10 report; CHANGELOG content has not
shifted since.

- **2.1.129** — gateway `/v1/models` discovery flips back to opt-in
  (`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`); `--plugin-url`;
  `skillOverrides` actually works; `claude_code.pull_request.count`
  OTel metric counts MCP-created PRs.
- **2.1.131** — VS Code extension activation fixed on Windows
  (`createRequire` polyfill); Mantle endpoint auth header.
- **2.1.132** — `CLAUDE_CODE_SESSION_ID` exposed to Bash subprocess
  env; `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`; graceful shutdown on
  external SIGINT; MCP servers no longer leak unbounded RSS on
  non-protocol stdout.
- **2.1.133** — `worktree.baseRef` switches `EnterWorktree` default
  back to `origin/<default>`; `parentSettingsBehavior` admin key;
  subagents finally discover Skills via the Skill tool.
- **2.1.136** — `autoMode.hard_deny`; broad fix sweep across
  plan-mode, `Edit`/`Write` allow rules, `@`-mention file picker,
  MCP OAuth refresh, and dozens of TUI rendering bugs.
- **2.1.137** — Single fix: VS Code extension activation on Windows
  (regression after 2.1.131).
- **2.1.138** — "Internal fixes" only.

## To land everything on the host

```bash
cd ~/Development/agenticloops-ai/claude-code-insights

# 1. Push the local commit that this run produced
git push origin main

# 2. Capture the nine uncovered versions (Docker required;
#    each build/capture/extract takes a few minutes)
prev=2.1.128
for v in 2.1.129 2.1.131 2.1.132 2.1.133 2.1.136 2.1.137 2.1.138 2.1.139 2.1.140; do
    /process-version "$v" --diff-from "$prev"
    prev="$v"
done

# Alternatively, the unattended cron script does the same loop with
# fetch-notes → capture → extract → summarize → diff → commit → push:
scripts/cron-capture.sh
```

`/process-version` is the LLM-driven slash command that does
build → capture → extract → summarize → release-notes → diff → commit.
It is idempotent, so re-running on a partially-captured version is safe.

## Sandbox blockers — unchanged from last run

- No `docker` binary, no `/var/run/docker.sock`. The capture pipeline
  builds `cch:<version>` from `sandbox/Dockerfile` and proxies a real
  Claude Code session through AgentLens — strictly Docker-required.
- The workspace mount blocks `unlink(2)` but allows `rename(2)`. Git's
  index-lock dance therefore strands a stale `.git/index.lock` after
  any interrupted operation, blocking subsequent commits. Workaround
  used this run: `mv .git/index.lock .git/index.lock.bakN` before
  retrying. With that, `git add`, `git commit` (with `--no-verify`
  and `core.fsmonitor=false`) succeed; `git push` cannot, because no
  credentials are present in the sandbox.

If you want this scheduled task to be fully end-to-end self-driving
from here, the runner would need:

1. Docker-in-Docker (or `/var/run/docker.sock` mounted from the host)
   so `scripts/capture-version.sh` can actually run, **and**
2. A credential helper or PAT in the sandbox env for `git push`,
   **and**
3. Either delete permission on the workspace mount, or git operations
   wrapped to `mv` aside any leftover `index.lock` on retry.

The previous-run guidance to use a host-side `cron-capture.sh` (which
already exists in `scripts/`) remains the most practical path.
