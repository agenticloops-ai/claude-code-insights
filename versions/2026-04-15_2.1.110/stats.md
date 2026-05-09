# claude-code 2.1.110 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 20 | 0 | 0 | 9 | 26300 | 3 | 3 | 13 | 3.8s |
| `03-with-mcp` | 2 | 10 | 20 | 0 | 0 | 9 | 26300 | 3 | 370 | 65 | 3.4s |
| `04-with-skill` | 3 | 10 | 20 | 0 | 0 | 9 | 26300 | 3 | 358 | 82 | 5.2s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
