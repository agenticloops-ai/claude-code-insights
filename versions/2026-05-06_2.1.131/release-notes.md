# claude-code 2.1.131

- **published:** 2026-05-06
- **source:** [CHANGELOG.md#21131](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#21131)
- **fetched:** 2026-05-12

- Fixed VS Code extension failing to activate on Windows due to a hardcoded build path in the bundled SDK (`createRequire` polyfill bug)
- Fixed Mantle endpoint authentication failing with missing `x-api-key` header
