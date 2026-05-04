# claude-code 2.1.51 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 8 | 0 | 0 | 0 | 2 | 18275 | 2 | 3 | 51 | 4.3s |
| `03-with-mcp` | 1 | 8 | 0 | 0 | 0 | 2 | 18275 | 2 | 3 | 3058 | 33.7s |
| `04-with-skill` | 3 | 8 | 0 | 0 | 0 | 2 | 18275 | 2 | 6 | 140 | 7.9s |

## Models seen across scenarios

- `claude-opus-4-6`
