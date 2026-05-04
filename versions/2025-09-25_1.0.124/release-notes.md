# claude-code 1.0.124

- **published:** 2025-09-25
- **source:** [CHANGELOG.md#10124](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#10124)
- **fetched:** 2026-05-03

- Set `CLAUDE_BASH_NO_LOGIN` environment variable to 1 or true to to skip login shell for BashTool
- Fix Bedrock and Vertex environment variables evaluating all strings as truthy
- No longer inform Claude of the list of allowed tools when permission is denied
- Fixed security vulnerability in Bash tool permission checks
- Improved VSCode extension performance for large files
