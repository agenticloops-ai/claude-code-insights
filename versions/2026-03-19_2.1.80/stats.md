# claude-code 2.1.80 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 0 | 0 | 0 | 5 | 15996 | 2 | 3 | 41 | 3.9s |
| `03-with-mcp` | 1 | 1 | 0 | 0 | 0 | 5 | 15996 | 2 | 3 | 51 | 3.1s |
| `04-with-skill` | 3 | 1 | 0 | 0 | 0 | 5 | 15996 | 2 | 8 | 142 | 6.9s |

## Models seen across scenarios

- `claude-opus-4-6`
