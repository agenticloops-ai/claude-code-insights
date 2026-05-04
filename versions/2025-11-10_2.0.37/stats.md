# claude-code 2.0.37 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 10512 | 0 | 461 | 150 | 4.7s |
| `03-with-mcp` | 3 | 16 | 0 | 0 | 0 | 0 | 10512 | 0 | 461 | 155 | 4.5s |
| `04-with-skill` | 5 | 16 | 0 | 0 | 0 | 0 | 10512 | 0 | 929 | 375 | 11.4s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
