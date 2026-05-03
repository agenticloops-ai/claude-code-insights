# claude-code 0.2.126 — capture summary

Baseline scenario: `01-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 12996 | 0 | 0 | 0 | 0.6s |
| `02-agent-task` | 3 | 15 | 0 | 0 | 0 | 0 | 12996 | 0 | 0 | 0 | 0.7s |
| `03-with-mcp-3tools` | 3 | 15 | 0 | 3 | 0 | 0 | 12996 | 0 | 0 | 0 | 0.7s |
| `04-with-skill` | 3 | 15 | 0 | 0 | 0 | 0 | 12996 | 0 | 0 | 0 | 0.6s |
| `05-many-tools-30` | 3 | 15 | 0 | 30 | 0 | 0 | 12996 | 0 | 0 | 0 | 0.7s |
| `06-plan-mode` | — | — | — | — | — | — | — | — | — | — | _no API requests_ |
| `07-cli-help` | _local_ | — | — | — | — | — | 2313 chars / 41 lines | — | — | — | exit 0 |
| `08-websearch` | 3 | 15 | 0 | 0 | 0 | 0 | 12996 | 0 | 0 | 0 | 0.6s |
| `09-mcp-help` | _local_ | — | — | — | — | — | 957 chars / 17 lines | — | — | — | exit 0 |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-3-7-sonnet-20250219`
