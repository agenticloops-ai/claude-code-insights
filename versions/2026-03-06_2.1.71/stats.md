# claude-code 2.1.71 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 0 | 0 | 0 | 4 | 19161 | 2 | 3 | 12 | 3.2s |
| `03-with-mcp` | 1 | 1 | 0 | 0 | 0 | 4 | 19161 | 2 | 3 | 1551 | 14.5s |
| `04-with-skill` | 3 | 1 | 0 | 0 | 0 | 4 | 19161 | 2 | 8 | 141 | 7.3s |

## Models seen across scenarios

- `claude-opus-4-6`
