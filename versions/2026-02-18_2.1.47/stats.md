# claude-code 2.1.47 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 23 | 0 | 0 | 0 | 2 | 18487 | 2 | 11 | 14 | 3.2s |
| `03-with-mcp` | 2 | 23 | 0 | 0 | 0 | 2 | 18487 | 2 | 11 | 1556 | 23.1s |
| `04-with-skill` | 3 | 23 | 0 | 0 | 0 | 2 | 18487 | 2 | 13 | 68 | 5.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
