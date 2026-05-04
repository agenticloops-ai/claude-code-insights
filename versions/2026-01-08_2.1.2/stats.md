# claude-code 2.1.2 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 12 | 131 | 4.3s |
| `03-with-mcp` | 5 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 3768 | 437 | 11.3s |
| `04-with-skill` | 6 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 3768 | 380 | 13.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
