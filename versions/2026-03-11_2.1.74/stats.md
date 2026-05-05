# claude-code 2.1.74 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 27 | 0 | 0 | 4 | 19284 | 2 | 3 | 13 | 2.7s |
| `03-with-mcp` | 1 | 1 | 27 | 0 | 0 | 4 | 19284 | 2 | 3 | 1571 | 18.2s |
| `04-with-skill` | 3 | 1 | 27 | 0 | 0 | 4 | 19284 | 2 | 8 | 142 | 7.2s |

## Models seen across scenarios

- `claude-opus-4-6`
