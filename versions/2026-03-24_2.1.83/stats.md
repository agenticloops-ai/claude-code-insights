# claude-code 2.1.83 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 0 | 0 | 0 | 6 | 30064 | 2 | 3 | 31 | 6.0s |
| `03-with-mcp` | 1 | 1 | 0 | 0 | 0 | 6 | 30064 | 2 | 3 | 1480 | 14.4s |
| `04-with-skill` | 3 | 1 | 0 | 0 | 0 | 6 | 30064 | 2 | 8 | 142 | 8.6s |

## Models seen across scenarios

- `claude-opus-4-6`
