# claude-code 2.0.60 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 18 | 0 | 0 | 0 | 0 | 12483 | 0 | 10 | 13 | 2.0s |
| `03-with-mcp` | 3 | 18 | 0 | 0 | 0 | 0 | 12483 | 0 | 738 | 234 | 6.1s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 12483 | 0 | 1594 | 283 | 9.5s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
