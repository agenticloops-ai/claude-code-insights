# claude-code 2.1.87 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 20 | 0 | 0 | 6 | 29226 | 2 | 3 | 13 | 10.3s |
| `03-with-mcp` | 1 | 9 | 20 | 0 | 0 | 6 | 29226 | 2 | 3 | 1578 | 15.0s |
| `04-with-skill` | 2 | 9 | 20 | 0 | 0 | 6 | 29226 | 2 | 5 | 66 | 3.5s |

## Models seen across scenarios

- `claude-opus-4-6`
