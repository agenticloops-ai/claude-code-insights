# claude-code 2.0.54 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 17 | 0 | 0 | 0 | 0 | 12413 | 0 | 668 | 121 | 4.3s |
| `03-with-mcp` | 4 | 17 | 0 | 0 | 0 | 0 | 12413 | 0 | 1513 | 307 | 9.7s |
| `04-with-skill` | 5 | 17 | 0 | 0 | 0 | 0 | 12413 | 0 | 1513 | 295 | 11.6s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
