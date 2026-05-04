# claude-code 1.0.8

- **published:** 2025-06-02
- **source:** [CHANGELOG.md#108](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#108)
- **fetched:** 2026-05-03

- Fixed Vertex AI region fallback when using CLOUD_ML_REGION
- Increased default otel interval from 1s -> 5s
- Fixed edge cases where MCP_TIMEOUT and MCP_TOOL_TIMEOUT weren't being respected
- Fixed a regression where search tools unnecessarily asked for permissions
- Added support for triggering thinking non-English languages
- Improved compacting UI
