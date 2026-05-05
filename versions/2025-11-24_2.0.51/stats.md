# claude-code 2.0.51 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 17 | 0 | 0 | 0 | 0 | 12413 | 0 | 660 | 115 | 2.9s |
| `03-with-mcp` | 3 | 17 | 0 | 0 | 0 | 0 | 12413 | 0 | 668 | 188 | 4.9s |
| `04-with-skill` | 5 | 17 | 0 | 0 | 0 | 0 | 12413 | 0 | 1513 | 339 | 10.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
