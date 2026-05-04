# claude-code 2.1.58 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 8 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 12 | 2.9s |
| `03-with-mcp` | 1 | 8 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 2931 | 32.7s |
| `04-with-skill` | 3 | 8 | 0 | 0 | 0 | 2 | 18738 | 2 | 6 | 141 | 14.7s |

## Models seen across scenarios

- `claude-opus-4-6`
