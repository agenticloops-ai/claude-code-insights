# claude-code 2.0.1 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 12339 | 1 | 2 | 12 | 2.0s |
| `03-with-mcp` | 2 | 15 | 0 | 0 | 0 | 0 | 12339 | 1 | 2 | 29 | 2.4s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-sonnet-4-5-20250929`
