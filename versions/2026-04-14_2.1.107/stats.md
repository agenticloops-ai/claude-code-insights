# claude-code 2.1.107 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 10 | 0 | 0 | 0 | 6 | 26300 | 3 | 342 | 25 | 3.2s |
| `03-with-mcp` | 2 | 10 | 0 | 0 | 0 | 6 | 26300 | 3 | 370 | 1581 | 15.3s |
| `04-with-skill` | 3 | 10 | 0 | 0 | 0 | 6 | 26300 | 3 | 358 | 82 | 5.3s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
