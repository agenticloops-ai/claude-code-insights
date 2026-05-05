# claude-code 2.1.89 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 20 | 0 | 0 | 6 | 29258 | 2 | 3 | 13 | 1.8s |
| `03-with-mcp` | 1 | 9 | 20 | 0 | 0 | 6 | 29258 | 2 | 3 | 1509 | 14.0s |
| `04-with-skill` | 2 | 9 | 20 | 0 | 0 | 6 | 29258 | 2 | 5 | 66 | 4.0s |

## Models seen across scenarios

- `claude-opus-4-6`
