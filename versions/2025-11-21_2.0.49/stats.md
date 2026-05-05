# claude-code 2.0.49 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 16 | 0 | 0 | 0 | 0 | 12417 | 0 | 1337 | 384 | 14.5s |
| `03-with-mcp` | 3 | 16 | 0 | 0 | 0 | 0 | 12417 | 0 | 668 | 170 | 5.1s |
| `04-with-skill` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.6s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
