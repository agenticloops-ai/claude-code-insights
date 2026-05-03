# claude-code 2.0.0 — capture summary

Baseline scenario: `01-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 12339 | 1 | 2 | 12 | 2.3s |
| `02-agent-task` | 3 | 15 | 0 | 0 | 0 | 0 | 12339 | 1 | 8 | 1483 | 21.4s |
| `03-with-mcp-3tools` | 2 | 15 | 0 | 3 | 0 | 0 | 12339 | 1 | 2 | 38 | 3.1s |
| `04-with-skill` | 2 | 15 | 0 | 0 | 0 | 0 | 12339 | 1 | 2 | 5 | 1.7s |
| `05-many-tools-30` | 2 | 15 | 0 | 30 | 0 | 0 | 12339 | 1 | 2 | 272 | 4.1s |
| `06-plan-mode` | 6 | 15 | 0 | 0 | 0 | 0 | 12339 | 2 | 14 | 923 | 24.5s |
| `07-cli-help` | _local_ | — | — | — | — | — | 4857 chars / 45 lines | — | — | — | exit 0 |
| `08-websearch` | 7 | 15 | 0 | 0 | 0 | 0 | 12415 | 1 | 21 | 570 | 16.1s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-sonnet-4-5-20250929`
