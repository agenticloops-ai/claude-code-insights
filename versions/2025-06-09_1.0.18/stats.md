# claude-code 1.0.18 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 16 | 1.9s |
| `03-with-mcp` | 2 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 75 | 4.6s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
