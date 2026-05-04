# claude-code 2.0.17 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 10177 | 0 | 406 | 217 | 6.1s |
| `03-with-mcp` | 3 | 15 | 0 | 0 | 0 | 0 | 10177 | 0 | 406 | 179 | 4.5s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
