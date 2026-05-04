# claude-code 2.0.41 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 16 | 0 | 0 | 0 | 0 | 10500 | 0 | 1201 | 298 | 8.6s |
| `03-with-mcp` | 2 | 16 | 0 | 0 | 0 | 0 | 10500 | 0 | 10 | 30 | 2.5s |
| `04-with-skill` | 5 | 16 | 0 | 0 | 0 | 0 | 10500 | 0 | 1207 | 494 | 13.2s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
