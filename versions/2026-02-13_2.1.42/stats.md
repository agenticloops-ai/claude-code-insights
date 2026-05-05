# claude-code 2.1.42 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 23 | 0 | 0 | 0 | 1 | 18487 | 2 | 11 | 13 | 3.7s |
| `03-with-mcp` | 2 | 23 | 0 | 0 | 0 | 1 | 18487 | 2 | 11 | 1499 | 22.9s |
| `04-with-skill` | 3 | 23 | 0 | 0 | 0 | 1 | 18487 | 2 | 13 | 67 | 5.6s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
