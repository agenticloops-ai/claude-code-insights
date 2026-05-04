# claude-code 2.0.43

- **published:** 2025-11-17
- **source:** [CHANGELOG.md#2043](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2043)
- **fetched:** 2026-05-03

- Added `permissionMode` field for custom agents
- Added `tool_use_id` field to `PreToolUseHookInput` and `PostToolUseHookInput` types
- Added skills frontmatter field to declare skills to auto-load for subagents
- Added the `SubagentStart` hook event
- Fixed nested `CLAUDE.md` files not loading when @-mentioning files
- Fixed duplicate rendering of some messages in the UI
- Fixed some visual flickers
- Fixed NotebookEdit tool inserting cells at incorrect positions when cell IDs matched the pattern `cell-N`
