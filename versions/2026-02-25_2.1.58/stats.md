# claude-code 2.1.58 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 2 | 15218 | 2 | 3 | 13 | 2.2s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 2 | 15218 | 2 | 3 | 133 | 13.4s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 2 | 15218 | 2 | 5 | 67 | 5.1s |

## Models seen across scenarios

- `claude-opus-4-6`
