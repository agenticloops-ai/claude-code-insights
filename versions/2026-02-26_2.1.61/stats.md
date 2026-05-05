# claude-code 2.1.61 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 24 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 13 | 2.6s |
| `03-with-mcp` | 1 | 24 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 1544 | 21.3s |
| `04-with-skill` | 2 | 24 | 0 | 0 | 0 | 2 | 18738 | 2 | 5 | 67 | 4.7s |

## Models seen across scenarios

- `claude-opus-4-6`
