# claude-code 2.0.65

- **published:** 2025-12-11
- **source:** [CHANGELOG.md#2065](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2065)
- **fetched:** 2026-05-03

- Added ability to switch models while writing a prompt using alt+p (linux, windows), option+p (macos).
- Added context window information to status line input
- Added `fileSuggestion` setting for custom `@` file search commands
- Added `CLAUDE_CODE_SHELL` environment variable to override automatic shell detection (useful when login shell differs from actual working shell)
- Fixed prompt not being saved to history when aborting a query with Escape
- Fixed Read tool image handling to identify format from bytes instead of file extension
