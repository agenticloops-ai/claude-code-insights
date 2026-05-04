# claude-code 1.0.48

- **published:** 2025-07-10
- **source:** [CHANGELOG.md#1048](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#1048)
- **fetched:** 2026-05-03

- Fixed a bug in v1.0.45 where the app would sometimes freeze on launch
- Added progress messages to Bash tool based on the last 5 lines of command output
- Added expanding variables support for MCP server configuration
- Moved shell snapshots from /tmp to ~/.claude for more reliable Bash tool calls
- Improved IDE extension path handling when Claude Code runs in WSL
- Hooks: Added a PreCompact hook
- Vim mode: Added c, f/F, t/T
