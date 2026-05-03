# claude-code 2.1.126 — capture summary

Baseline scenario: `01-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01-bare` | 1 | 10 | 17 | 0 | 1 | 11 | 26719 | 3 | 6 | 15 | 1.3s |
| `02-agent-task` | 6 | 10 | 17 | 0 | 1 | 11 | 26719 | 3 | 387 | 6356 | 64.9s |
| `03-with-mcp-3tools` | 2 | 10 | 17 | 0 | 4 | 11 | 26719 | 3 | 373 | 67 | 3.7s |
| `04-with-skill` | 2 | 10 | 17 | 0 | 1 | 11 | 26719 | 3 | 11 | 137 | 3.5s |
| `05-many-tools-30` | 2 | 10 | 17 | 0 | 31 | 11 | 26719 | 3 | 376 | 406 | 4.8s |
| `06-plan-mode` | 11 | 10 | 17 | 0 | 1 | 11 | 26719 | 4 | 405 | 4965 | 80.9s |
| `07-cli-help` | _local_ | — | — | — | — | — | 9545 chars / 74 lines | — | — | — | exit 0 |
| `08-websearch` | 5 | 10 | 17 | 0 | 1 | 11 | 26719 | 3 | 389 | 452 | 10.4s |
| `09-mcp-help` | _local_ | — | — | — | — | — | 1782 chars / 30 lines | — | — | — | exit 0 |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
