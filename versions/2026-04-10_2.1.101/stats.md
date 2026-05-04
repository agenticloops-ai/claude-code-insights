# claude-code 2.1.101 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 0 | 0 | 0 | 6 | 26300 | 3 | 3 | 13 | 3.6s |
| `03-with-mcp` | 1 | 10 | 0 | 0 | 0 | 6 | 26300 | 3 | 3 | 1568 | 14.3s |
| `04-with-skill` | 2 | 10 | 0 | 0 | 0 | 6 | 26300 | 3 | 5 | 66 | 6.0s |

## Models seen across scenarios

- `claude-opus-4-6`
