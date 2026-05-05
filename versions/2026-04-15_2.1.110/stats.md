# claude-code 2.1.110 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 22 | 0 | 0 | 9 | 26300 | 4 | 3 | 13 | 3.4s |
| `03-with-mcp` | 2 | 10 | 22 | 0 | 0 | 9 | 26300 | 4 | 370 | 1592 | 16.4s |
| `04-with-skill` | 3 | 10 | 22 | 0 | 0 | 9 | 26300 | 4 | 358 | 82 | 5.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
