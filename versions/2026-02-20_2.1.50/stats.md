# claude-code 2.1.50 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 2 | 18275 | 2 | 3 | 53 | 3.1s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 2 | 18275 | 2 | 3 | 1554 | 23.3s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 2 | 18275 | 2 | 5 | 97 | 6.6s |

## Models seen across scenarios

- `claude-opus-4-6`
