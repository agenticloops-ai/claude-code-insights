# claude-code 2.1.66 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 3 | 15379 | 2 | 3 | 115 | 6.2s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 3 | 15379 | 2 | 3 | 134 | 6.7s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 3 | 15379 | 2 | 5 | 66 | 5.6s |

## Models seen across scenarios

- `claude-opus-4-6`
