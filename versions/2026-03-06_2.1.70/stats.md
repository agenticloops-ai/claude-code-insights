# claude-code 2.1.70 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 21 | 0 | 0 | 3 | 15641 | 2 | 3 | 13 | 1.5s |
| `03-with-mcp` | 1 | 1 | 21 | 0 | 0 | 3 | 15641 | 2 | 3 | 51 | 2.6s |
| `04-with-skill` | 3 | 1 | 21 | 0 | 0 | 3 | 15641 | 2 | 8 | 142 | 6.7s |

## Models seen across scenarios

- `claude-opus-4-6`
