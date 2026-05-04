# claude-code 2.1.108 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 0 | 0 | 0 | 12 | 26300 | 3 | 3 | 36 | 2.9s |
| `03-with-mcp` | 2 | 10 | 0 | 0 | 0 | 12 | 26300 | 3 | 370 | 1241 | 13.4s |
| `04-with-skill` | 3 | 10 | 0 | 0 | 0 | 12 | 26300 | 3 | 358 | 82 | 5.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
