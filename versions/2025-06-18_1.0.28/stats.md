# claude-code 1.0.28 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 16 | 0 | 0 | 0 | 0 | 13031 | 1 | 2 | 12 | 1.8s |
| `03-with-mcp` | 2 | 16 | 0 | 0 | 0 | 0 | 13031 | 1 | 2 | 81 | 5.1s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
