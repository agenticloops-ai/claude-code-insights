# claude-code 2.1.62 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 13 | 2.0s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 2 | 18738 | 2 | 3 | 1554 | 22.2s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 2 | 18738 | 2 | 5 | 66 | 24.0s |

## Models seen across scenarios

- `claude-opus-4-6`
