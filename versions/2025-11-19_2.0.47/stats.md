# claude-code 2.0.47 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 12417 | 0 | 600 | 196 | 5.5s |
| `03-with-mcp` | 2 | 16 | 0 | 0 | 0 | 0 | 12417 | 0 | 10 | 30 | 3.8s |
| `04-with-skill` | 5 | 16 | 0 | 0 | 0 | 0 | 12417 | 0 | 1207 | 307 | 10.4s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
