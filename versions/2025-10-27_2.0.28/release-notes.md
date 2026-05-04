# claude-code 2.0.28

- **published:** 2025-10-27
- **source:** [CHANGELOG.md#2028](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2028)
- **fetched:** 2026-05-03

- Plan mode: introduced new Plan subagent
- Subagents: claude can now choose to resume subagents
- Subagents: claude can dynamically choose the model used by its subagents
- SDK: added --max-budget-usd flag
- Discovery of custom slash commands, subagents, and output styles no longer respects .gitignore
- Stop `/terminal-setup` from adding backslash to `Shift + Enter` in VS Code
- Add branch and tag support for git-based plugins and marketplaces using fragment syntax (e.g., `owner/repo#branch`)
- Fixed a bug where macOS permission prompts would show up upon initial launch when launching from home directory
- Various other bug fixes
