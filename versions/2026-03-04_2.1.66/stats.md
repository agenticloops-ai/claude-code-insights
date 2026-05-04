# claude-code 2.1.66 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 3 | 18899 | 2 | 3 | 12 | 1.6s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 3 | 18899 | 2 | 3 | 3061 | 34.7s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 3 | 18899 | 2 | 5 | 66 | 4.5s |

## Models seen across scenarios

- `claude-opus-4-6`
