# claude-code 1.0.128 — capture summary

Baseline scenario: `01-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01-bare` | 2 | 16 | 0 | 0 | 0 | 0 | 13878 | 1 | 2 | 19 | 2.9s |
| `02-agent-task` | 26 | 16 | 0 | 0 | 0 | 0 | 13878 | 1 | 86 | 11256 | 204.2s |
| `03-with-mcp-3tools` | 2 | 16 | 0 | 3 | 0 | 0 | 13878 | 1 | 2 | 38 | 2.7s |
| `04-with-skill` | 2 | 16 | 0 | 0 | 0 | 0 | 13878 | 1 | 2 | 16 | 2.1s |
| `05-many-tools-30` | 2 | 16 | 0 | 30 | 0 | 0 | 13878 | 1 | 2 | 295 | 5.9s |
| `06-plan-mode` | 11 | 16 | 0 | 0 | 0 | 0 | 13878 | 2 | 14 | 957 | 58.6s |
| `07-cli-help` | _local_ | — | — | — | — | — | 4966 chars / 46 lines | — | — | — | exit 0 |
| `08-websearch` | 4 | 16 | 0 | 0 | 0 | 0 | 13954 | 1 | 10 | 609 | 22.7s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-1-20250805`
