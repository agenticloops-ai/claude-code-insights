# claude-code 2.0.47 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.6s |
| `03-with-mcp` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 1.5s |
| `04-with-skill` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
