# claude-code 2.0.52

- **published:** 2025-11-24
- **source:** [CHANGELOG.md#2052](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2052)
- **fetched:** 2026-05-03

- Fixed duplicate message display when starting Claude with a command line argument
- Fixed `/usage` command progress bars to fill up as usage increases (instead of showing remaining percentage)
- Fixed image pasting not working on Linux systems running Wayland (now falls back to wl-paste when xclip is unavailable)
- Permit some uses of `$!` in bash commands
