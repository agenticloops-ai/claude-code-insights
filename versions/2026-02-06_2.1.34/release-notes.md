# claude-code 2.1.34

- **published:** 2026-02-06
- **source:** [CHANGELOG.md#2134](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2134)
- **fetched:** 2026-05-04

- Fixed a crash when agent teams setting changed between renders
- Fixed a bug where commands excluded from sandboxing (via `sandbox.excludedCommands` or `dangerouslyDisableSandbox`) could bypass the Bash ask permission rule when `autoAllowBashIfSandboxed` was enabled
