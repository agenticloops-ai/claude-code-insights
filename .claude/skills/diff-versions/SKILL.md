---
name: diff-versions
description: Generate a markdown diff report between two extracted claude-code versions. Writes versions/<to>/diff-from-<from>.md (colocated with the newer version's artifacts). Use when comparing how the system prompt, tools, skills, or user-message reminders changed between releases. Both versions must already be extracted under versions/.
---

# diff-versions

Compare two `claude-code` versions that have already been processed by `extract-capture`. Produces a single markdown file at `versions/<to>/diff-from-<from>.md` summarizing what changed across every shared scenario.

## When to invoke

- The user asks to "diff", "compare", or "what changed between" two versions.
- A new version was just extracted and the user wants the changelog vs the previous one.
- Called by the `/process-version` orchestrator when `--diff-from` is supplied.

## How to run

1. Confirm both versions are extracted:
   ```bash
   ls versions/<from>/scenarios/*/stats.json versions/<to>/scenarios/*/stats.json 2>/dev/null | head
   ```
   If either version is missing `stats.json` files, run the `extract-capture` skill on it first (or `/process-version` end-to-end).
2. Generate the diff:
   ```bash
   python3 scripts/diff-versions.py <from> <to>
   ```
   Writes `versions/<to>/diff-from-<from>.md`.
3. Open the file and summarize the most interesting findings to the user (don't dump the whole report). Useful angles:
   - net change in advertised vs deferred tool counts
   - newly added or removed tools, especially when something moved to/from `ToolSearch`
   - new built-in skills
   - system-prompt sections added/removed (look for new `# ...` headings in the diff)
   - reminder-block changes (visible inside the user-prompt diff)

## Output structure

Each shared scenario gets:

```
## scenario: <name>

| metric        | <from> | <to> |
| ...

### built-in skills        (added / removed / description-changed)
### tools                  (added / removed / moved-to-deferred / moved-to-advertised / new-deferred / modified)
### system prompt          (unified diff)
### user prompt (incl. system-reminder blocks)   (unified diff)
```

The local-mode CLI scenario (`07-cli-help`) also gets diffed: parsed added/removed flags + commands, plus the raw unified diff inside a collapsed `<details>` block.

## Notes

- The diff is purely textual on the *extracted* artifacts. If a scenario's `stats.json` looks identical but the diff body is empty, that's expected — nothing observable changed.
- Scenarios present in only one version are listed at the top under "only in `<version>`" and not diffed.
- The diff reads only from `versions/`; the raw `<scenario>.json` session captures and per-request `001.*.json` files are not consulted.
