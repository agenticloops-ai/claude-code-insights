---
description: Regenerate VERSIONS.md from npm + the upstream Claude Code CHANGELOG
allowed-tools: Bash(python3 scripts/refresh-versions.py), Bash(git diff --stat VERSIONS.md), Bash(git diff VERSIONS.md)
---

Run `python3 scripts/refresh-versions.py`, then show me `git diff --stat VERSIONS.md` so I can see what changed. If new versions appeared, also show the first 30 lines of `git diff VERSIONS.md`.
