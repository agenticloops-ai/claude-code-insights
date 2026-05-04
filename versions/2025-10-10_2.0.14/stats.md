# claude-code 2.0.14 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 9583 | 0 | 2 | 87 | 3.1s |
| `03-with-mcp` | 2 | 15 | 0 | 0 | 0 | 0 | 9583 | 0 | 2 | 29 | 2.0s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-sonnet-4-5-20250929`
