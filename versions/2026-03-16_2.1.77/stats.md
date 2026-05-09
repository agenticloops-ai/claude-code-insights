# claude-code 2.1.77 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 25 | 0 | 0 | 5 | 15786 | 2 | 3 | 13 | 1.6s |
| `03-with-mcp` | 1 | 1 | 25 | 0 | 0 | 5 | 15786 | 2 | 3 | 50 | 1.9s |
| `04-with-skill` | 3 | 1 | 25 | 0 | 0 | 5 | 15786 | 2 | 8 | 141 | 29.4s |

## Models seen across scenarios

- `claude-opus-4-6`
