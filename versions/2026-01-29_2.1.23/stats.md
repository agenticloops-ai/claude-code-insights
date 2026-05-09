# claude-code 2.1.23 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 17 | 0 | 0 | 0 | 1 | 12886 | 1 | 11 | 18 | 3.1s |
| `03-with-mcp` | 1 | 17 | 0 | 0 | 0 | 1 | 12850 | 1 | 3 | 29 | 1.9s |
| `04-with-skill` | 3 | 17 | 0 | 0 | 0 | 1 | 12850 | 1 | 13 | 65 | 4.1s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
