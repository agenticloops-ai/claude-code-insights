# claude-code 2.0.31 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 10511 | 0 | 461 | 244 | 6.2s |
| `03-with-mcp` | 4 | 16 | 0 | 0 | 0 | 0 | 10511 | 0 | 923 | 208 | 9.4s |
| `04-with-skill` | 5 | 16 | 0 | 0 | 0 | 0 | 10511 | 0 | 929 | 298 | 11.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
