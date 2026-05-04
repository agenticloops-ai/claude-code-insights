# claude-code 1.0.17 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 25 | 2.3s |
| `04-agent-task` | 11 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 23 | 2885 | 61.4s |
| `03-with-mcp` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 29 | 2.5s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
