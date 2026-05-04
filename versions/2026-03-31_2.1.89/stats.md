# claude-code 2.1.89 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 0 | 0 | 0 | 6 | 29258 | 2 | 3 | 13 | 4.1s |
| `03-with-mcp` | 1 | 9 | 0 | 0 | 0 | 6 | 29258 | 2 | 3 | 1564 | 14.8s |
| `04-with-skill` | 2 | 9 | 0 | 0 | 0 | 6 | 29258 | 2 | 5 | 66 | 4.5s |

## Models seen across scenarios

- `claude-opus-4-6`
