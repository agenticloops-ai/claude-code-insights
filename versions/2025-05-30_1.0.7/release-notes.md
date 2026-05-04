# claude-code 1.0.7

- **published:** 2025-05-30
- **source:** [CHANGELOG.md#107](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#107)
- **fetched:** 2026-05-03

- Renamed /allowed-tools -> /permissions
- Migrated allowedTools and ignorePatterns from .claude.json -> settings.json
- Deprecated claude config commands in favor of editing settings.json
- Fixed a bug where --dangerously-skip-permissions sometimes didn't work in --print mode
- Improved error handling for /install-github-app
- Bugfixes, UI polish, and tool reliability improvements
