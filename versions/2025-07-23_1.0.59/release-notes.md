# claude-code 1.0.59

- **published:** 2025-07-23
- **source:** [CHANGELOG.md#1059](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#1059)
- **fetched:** 2026-05-03

- SDK: Added tool confirmation support with canUseTool callback
- SDK: Allow specifying env for spawned process
- Hooks: Exposed PermissionDecision to hooks (including "ask")
- Hooks: UserPromptSubmit now supports additionalContext in advanced JSON output
- Fixed issue where some Max users that specified Opus would still see fallback to Sonnet
