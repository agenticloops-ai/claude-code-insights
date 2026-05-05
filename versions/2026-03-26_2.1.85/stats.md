# claude-code 2.1.85 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 20 | 0 | 0 | 6 | 28767 | 2 | 3 | 42 | 3.0s |
| `03-with-mcp` | 1 | 9 | 20 | 0 | 0 | 6 | 29147 | 2 | 3 | 1545 | 14.8s |
| `04-with-skill` | 2 | 9 | 20 | 0 | 0 | 6 | 29147 | 2 | 5 | 66 | 10.8s |

## Models seen across scenarios

- `claude-opus-4-6`
