# claude-code 2.0.68

- **published:** 2025-12-12
- **source:** [CHANGELOG.md#2068](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2068)
- **fetched:** 2026-05-03

- Fixed IME (Input Method Editor) support for languages like Chinese, Japanese, and Korean by correctly positioning the composition window at the cursor
- Fixed a bug where disallowed MCP tools were visible to the model
- Fixed an issue where steering messages could be lost while a subagent is working
- Fixed Option+Arrow word navigation treating entire CJK (Chinese, Japanese, Korean) text sequences as a single word instead of navigating by word boundaries
- Improved plan mode exit UX: show simplified yes/no dialog when exiting with empty or missing plan instead of throwing an error
- Add support for enterprise managed settings. Contact your Anthropic account team to enable this feature.
