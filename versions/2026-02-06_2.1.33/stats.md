# claude-code 2.1.33 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 23 | 0 | 0 | 0 | 1 | 17525 | 1 | 11 | 13 | 3.2s |
| `03-with-mcp` | 2 | 23 | 0 | 0 | 0 | 1 | 17525 | 1 | 11 | 1405 | 19.7s |
| `04-with-skill` | 3 | 23 | 0 | 0 | 0 | 1 | 17525 | 1 | 13 | 66 | 4.5s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
