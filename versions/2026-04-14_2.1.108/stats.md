# claude-code 2.1.108 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 21 | 0 | 0 | 12 | 26300 | 3 | 3 | 13 | 2.6s |
| `03-with-mcp` | 2 | 10 | 21 | 0 | 0 | 12 | 26300 | 3 | 370 | 1619 | 23.3s |
| `04-with-skill` | 3 | 10 | 21 | 0 | 0 | 12 | 26300 | 3 | 358 | 82 | 5.6s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
