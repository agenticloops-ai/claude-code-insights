# claude-code 0.2.93 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 14 | 0 | 0 | 0 | 0 | 12914 | 0 | 0 | 0 | 0.7s |
| `04-agent-task` | 3 | 14 | 0 | 0 | 0 | 0 | 12914 | 0 | 0 | 0 | 0.8s |
| `03-with-mcp` | 3 | 14 | 0 | 0 | 0 | 0 | 12914 | 0 | 0 | 0 | 0.9s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-3-7-sonnet-20250219`
