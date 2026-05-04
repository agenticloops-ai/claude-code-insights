# claude-code 2.0.30 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 10358 | 0 | 409 | 201 | 5.6s |
| `03-with-mcp` | 3 | 16 | 0 | 0 | 0 | 0 | 10358 | 0 | 409 | 207 | 4.8s |
| `04-with-skill` | 5 | 16 | 0 | 0 | 0 | 0 | 10358 | 0 | 825 | 334 | 15.1s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
