---
name: process-version
description: End-to-end automation for one claude-code release — fetch upstream release notes first, surface and (with user approval) enable any new opt-in feature flags in sandbox settings, then capture every scenario, extract artifacts, summarize, and (optionally) diff against a previous version. Invoke as /process-version <version> [--diff-from <prev>]. Use when the user wants to "process", "snapshot", or "fully capture" a version, or when a new release just landed and they want the changelog refresh.
---

# process-version

Single entry point for capturing and analyzing one `claude-code` release. The skill itself owns orchestration; shell and Python scripts under `scripts/` and `sandbox/` stay as primitives this skill drives via the Bash and Skill tools.

## Inputs

- `<version>` — the npm version of `@anthropic-ai/claude-code` (e.g. `2.1.126`). Required.
- `--diff-from <prev>` — optional previous version to diff against (e.g. `2.1.59`).

## Pipeline

Run these steps in order. Each step runs via the Bash tool unless otherwise noted. **Do not parallelize** — later steps depend on earlier outputs.

### 1. Pre-flight: fetch release notes and scan for new feature flags

```bash
python3 scripts/fetch-release-notes.py <version>
```

Writes `versions/<version>/release-notes.md` *before* capture so the next step can read it. If the upstream `CHANGELOG.md` has no entry for this version (silent patch), the file contains a one-line placeholder — that is success, not failure, and step 2 has nothing to do.

### 2. Surface and (with user approval) enable new feature flags

Read `versions/<version>/release-notes.md` and grep for indicators of opt-in features that wouldn't be exercised by a default-config capture:

- `CLAUDE_CODE_*` env vars (especially `CLAUDE_CODE_EXPERIMENTAL_*`).
- Phrases like "research preview", "disabled by default", "opt-in", "experimental", "feature flag", "enable with", "set X to", "add to settings.json".
- New CLI flags described as gating capability (e.g. "pass `--enable-foo` to ...").

For each candidate, check whether `sandbox/fixtures/home/.claude/settings.json` already enables it (read the file). If not:

1. List the candidates and the proposed settings change to the user via `AskUserQuestion`. Include the upstream phrasing verbatim.
2. **Only on user confirmation**, edit `sandbox/fixtures/home/.claude/settings.json` to add the flag. Env vars go under the top-level `"env"` object as `"VAR_NAME": "1"` (string value); other settings go at the appropriate key.
3. If the user declines, capture proceeds with default config — note in the final report that the new feature wasn't exercised so the diff won't reflect it.

If no candidates are found, skip silently and continue to step 3.

### 3. Capture every scenario

```bash
scripts/capture-version.sh <version>
```

Runs each `scenarios/<NN>-<name>/` against the pinned `cch:<version>` Docker image. Continues on per-scenario failure; final summary line lists `passed:`, `skipped:`, and `failed:` scenario names. `skipped:` means the scenario's `min_version` is above the target — that's expected on older releases (e.g. `04-with-skill` pre-2.0.28) and is not an error. Capture the exit code and the three summary lines for the final report.

If `02-bare` is among `failed:`, the rest of the pipeline (specifically `summarize-version.py`) cannot run — abort with a clear message naming the failed scenarios.

### 4. Extract every fresh capture

Invoke the **`extract-capture`** skill via the Skill tool, passing the version. The skill loops `versions/<version>/scenarios/*/` and calls `scripts/extract.py` for each, skipping local-mode scenarios that have only `output.txt`. Track which scenarios extract failures came back from; surface them in the final report but don't abort.

### 5. Summarize

```bash
python3 scripts/summarize-version.py <version>
```

Promotes the baseline scenario's extracted artifacts to `versions/<version>/` root and writes `manifest.json` + `stats.md`. If `02-bare` extraction is missing this script will `sys.exit`; that's why step 3 must guarantee it's present.

### 6. Diff (only if `--diff-from <prev>` given)

Invoke the **`diff-versions`** skill via the Skill tool with `(prev, version)`. The skill runs `scripts/diff-versions.py prev version`, which writes `versions/<version>/diff-from-<prev>.md`.

## Final report

After all steps, emit a short summary (no file dumps):

- `version: <version>`
- `release-notes: versions/<version>/release-notes.md` (note "no upstream entry" if placeholder)
- `feature flags: <enabled / declined / none found>` — list any settings.json edits made or skipped
- `capture: <N> passed, <M> failed (<list>)`
- `extract: <N> succeeded, <M> failed (<list>)`
- `manifest: versions/<version>/manifest.json`
- `diff: versions/<version>/diff-from-<prev>.md` (only when `--diff-from` was given)

If anything failed, end with the next concrete action the user can take (e.g. "re-run scenario X with `CAPTURE_KEEP_STATE=1` to keep state for debugging").

## Notes

- Docker is required (the sandbox image is built on demand by `sandbox/build.sh`). If `docker` is unavailable, surface the error from `capture-version.sh` immediately rather than retrying.
- Auth: `cch-auth` Docker volume must already hold OAuth credentials (`sandbox/login.sh <version>` populates it). If the capture errors with "WARN: cch-auth volume looks empty", tell the user to run login first.
- The pipeline is idempotent for already-captured versions; re-running overwrites `extracted/`, the version-root files, `manifest.json`, `stats.md`, and `diff-from-<prev>.md`. `release-notes.md` is also overwritten with a fresh fetch.
- Versions list itself (`VERSIONS.md`) is regenerated by a separate `/refresh-versions` slash command — not part of this pipeline.
