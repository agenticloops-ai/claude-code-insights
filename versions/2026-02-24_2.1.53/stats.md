# claude-code 2.1.53 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 8 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 12 | 3.9s |
| `03-with-mcp` | 1 | 8 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 3039 | 33.9s |
| `04-with-skill` | 3 | 8 | 0 | 0 | 0 | 2 | 18738 | 2 | 6 | 141 | 7.5s |

## Models seen across scenarios

- `claude-opus-4-6`
