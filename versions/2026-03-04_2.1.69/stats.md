# claude-code 2.1.69 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 23 | 0 | 0 | 3 | 19161 | 2 | 3 | 13 | 2.4s |
| `03-with-mcp` | 1 | 1 | 23 | 0 | 0 | 3 | 19161 | 2 | 3 | 1551 | 19.4s |
| `04-with-skill` | 3 | 1 | 23 | 0 | 0 | 3 | 19161 | 2 | 6 | 141 | 6.5s |

## Models seen across scenarios

- `claude-opus-4-6`
