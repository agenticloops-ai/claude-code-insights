# claude-code 1.0.18

- **published:** 2025-06-09
- **source:** [CHANGELOG.md#1018](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#1018)
- **fetched:** 2026-05-03

- Added --add-dir CLI argument for specifying additional working directories
- Added streaming input support without require -p flag
- Improved startup performance and session storage performance
- Added CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR environment variable to freeze working directory for bash commands
- Added detailed MCP server tools display (/mcp)
- MCP authentication and permission improvements
- Added auto-reconnection for MCP SSE connections on disconnect
- Fixed issue where pasted content was lost when dialogs appeared
