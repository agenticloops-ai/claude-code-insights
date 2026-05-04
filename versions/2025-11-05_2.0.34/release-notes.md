# claude-code 2.0.34

- **published:** 2025-11-05
- **source:** [CHANGELOG.md#2034](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2034)
- **fetched:** 2026-05-03

- VSCode Extension: Added setting to configure the initial permission mode for new conversations
- Improved file path suggestion performance with native Rust-based fuzzy finder
- Fixed infinite token refresh loop that caused MCP servers with OAuth (e.g., Slack) to hang during connection
- Fixed memory crash when reading or writing large files (especially base64-encoded images)
