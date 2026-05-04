# claude-code 2.1.49 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 2 | 18487 | 2 | 3 | 13 | 17.5s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 2 | 18487 | 2 | 3 | 1555 | 20.9s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 2 | 18487 | 2 | 5 | 66 | 6.3s |

## Models seen across scenarios

- `claude-opus-4-6`
