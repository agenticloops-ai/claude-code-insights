# claude-code 1.0.11 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 12 | 2.1s |
| `04-agent-task` | 5 | 15 | 0 | 0 | 0 | 0 | 13225 | 1 | 8 | 1065 | 17.9s |
| `03-with-mcp` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 29 | 2.9s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
- `claude-sonnet-4-5-20250929`
