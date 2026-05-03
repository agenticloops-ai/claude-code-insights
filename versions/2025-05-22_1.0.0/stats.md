# claude-code 1.0.0 — capture summary

Baseline scenario: `01-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 2 | 27 | 3.0s |
| `02-agent-task` | 6 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 14 | 5505 | 93.4s |
| `03-with-mcp-3tools` | 2 | 15 | 0 | 3 | 0 | 0 | 12993 | 1 | 2 | 38 | 2.9s |
| `04-with-skill` | 2 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 2 | 16 | 1.9s |
| `05-many-tools-30` | 2 | 15 | 0 | 30 | 0 | 0 | 12993 | 1 | 2 | 272 | 5.8s |
| `06-plan-mode` | — | — | — | — | — | — | — | — | — | — | _no API requests_ |
| `07-cli-help` | _local_ | — | — | — | — | — | 2602 chars / 45 lines | — | — | — | exit 0 |
| `08-websearch` | 12 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 20 | 1514 | 54.0s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
