# claude-code 2.0.34 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 10515 | 0 | 461 | 188 | 6.6s |
| `03-with-mcp` | 3 | 16 | 0 | 0 | 0 | 0 | 10515 | 0 | 461 | 182 | 4.8s |
| `04-with-skill` | 4 | 16 | 0 | 0 | 0 | 0 | 10515 | 0 | 467 | 209 | 5.4s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
