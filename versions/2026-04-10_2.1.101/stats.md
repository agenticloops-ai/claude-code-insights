# claude-code 2.1.101 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 19 | 0 | 0 | 6 | 26300 | 2 | 3 | 13 | 2.3s |
| `03-with-mcp` | 1 | 10 | 19 | 0 | 0 | 6 | 26300 | 2 | 3 | 51 | 3.6s |
| `04-with-skill` | 2 | 10 | 19 | 0 | 0 | 6 | 26300 | 2 | 5 | 65 | 5.1s |

## Models seen across scenarios

- `claude-opus-4-6`
