# claude-code 2.1.74 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 0 | 0 | 0 | 4 | 19284 | 2 | 3 | 13 | 2.1s |
| `03-with-mcp` | 1 | 1 | 0 | 0 | 0 | 4 | 19284 | 2 | 3 | 1486 | 13.9s |
| `04-with-skill` | 3 | 1 | 0 | 0 | 0 | 4 | 19284 | 2 | 8 | 142 | 7.4s |

## Models seen across scenarios

- `claude-opus-4-6`
