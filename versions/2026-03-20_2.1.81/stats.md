# claude-code 2.1.81 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 26 | 0 | 0 | 5 | 15996 | 2 | 3 | 13 | 2.8s |
| `03-with-mcp` | 1 | 1 | 26 | 0 | 0 | 6 | 15996 | 2 | 3 | 51 | 2.4s |
| `04-with-skill` | 3 | 1 | 26 | 0 | 0 | 6 | 15996 | 2 | 8 | 142 | 132.6s |

## Models seen across scenarios

- `claude-opus-4-6`
