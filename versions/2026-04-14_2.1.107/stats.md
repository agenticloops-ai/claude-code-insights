# claude-code 2.1.107 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 10 | 19 | 0 | 0 | 6 | 26300 | 2 | 342 | 24 | 3.2s |
| `03-with-mcp` | 2 | 10 | 19 | 0 | 0 | 6 | 26300 | 2 | 370 | 64 | 3.4s |
| `04-with-skill` | 3 | 10 | 19 | 0 | 0 | 6 | 26300 | 2 | 358 | 82 | 11.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
