# claude-code 2.0.17

- **published:** 2025-10-15
- **source:** [CHANGELOG.md#2017](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2017)
- **fetched:** 2026-05-03

- Added Haiku 4.5 to model selector!
- Haiku 4.5 automatically uses Sonnet in plan mode, and Haiku for execution (i.e. SonnetPlan by default)
- 3P (Bedrock and Vertex) are not automatically upgraded yet. Manual upgrading can be done through setting `ANTHROPIC_DEFAULT_HAIKU_MODEL`
- Introducing the Explore subagent. Powered by Haiku it'll search through your codebase efficiently to save context!
- OTEL: support HTTP_PROXY and HTTPS_PROXY
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` now disables release notes fetching
