# claude-code 2.1.15

- **published:** 2026-01-21
- **source:** [CHANGELOG.md#2115](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2115)
- **fetched:** 2026-05-04

- Added deprecation notification for npm installations - run `claude install` or see https://docs.anthropic.com/en/docs/claude-code/getting-started for more options
- Improved UI rendering performance with React Compiler
- Fixed the "Context left until auto-compact" warning not disappearing after running `/compact`
- Fixed MCP stdio server timeout not killing child process, which could cause UI freezes
