# claude-code 2.0.71

- **published:** 2025-12-16
- **source:** [CHANGELOG.md#2071](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2071)
- **fetched:** 2026-05-03

- Added /config toggle to enable/disable prompt suggestions
- Added `/settings` as an alias for the `/config` command
- Fixed @ file reference suggestions incorrectly triggering when cursor is in the middle of a path
- Fixed MCP servers from `.mcp.json` not loading when using `--dangerously-skip-permissions`
- Fixed permission rules incorrectly rejecting valid bash commands containing shell glob patterns (e.g., `ls *.txt`, `for f in *.png`)
- Bedrock: Environment variable `ANTHROPIC_BEDROCK_BASE_URL` is now respected for token counting and inference profile listing
- New syntax highlighting engine for native build
