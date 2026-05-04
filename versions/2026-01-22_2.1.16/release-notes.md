# claude-code 2.1.16

- **published:** 2026-01-22
- **source:** [CHANGELOG.md#2116](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2116)
- **fetched:** 2026-05-04

- Added new task management system, including new capabilities like dependency tracking
- [VSCode] Added native plugin management support
- [VSCode] Added ability for OAuth users to browse and resume remote Claude sessions from the Sessions dialog
- Fixed out-of-memory crashes when resuming sessions with heavy subagent usage
- Fixed an issue where the "context remaining" warning was not hidden after running `/compact`
- Fixed session titles on the resume screen not respecting the user's language setting
- [IDE] Fixed a race condition on Windows where the Claude Code sidebar view container would not appear on start
