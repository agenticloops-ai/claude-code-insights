# claude-code 2.0.25 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 10017 | 0 | 409 | 239 | 6.5s |
| `03-with-mcp` | 3 | 16 | 0 | 0 | 0 | 0 | 10017 | 0 | 409 | 153 | 6.2s |
| `04-with-skill` | 4 | 16 | 0 | 0 | 0 | 0 | 10017 | 0 | 415 | 187 | 6.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
