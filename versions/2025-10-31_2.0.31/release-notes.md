# claude-code 2.0.31

- **published:** 2025-10-31
- **source:** [CHANGELOG.md#2031](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2031)
- **fetched:** 2026-05-03

- Windows: native installation uses shift+tab as shortcut for mode switching, instead of alt+m
- Vertex: add support for Web Search on supported models
- VSCode: Adding the respectGitIgnore configuration to include .gitignored files in file searches (defaults to true)
- Fixed a bug with subagents and MCP servers related to "Tool names must be unique" error
- Fixed issue causing `/compact` to fail with `prompt_too_long` by making it respect existing compact boundaries
- Fixed plugin uninstall not removing plugins
