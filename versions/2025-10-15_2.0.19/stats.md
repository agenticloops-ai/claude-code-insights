# claude-code 2.0.19 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 9851 | 0 | 409 | 163 | 4.6s |
| `03-with-mcp` | 3 | 15 | 0 | 0 | 0 | 0 | 9851 | 0 | 409 | 150 | 5.1s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
