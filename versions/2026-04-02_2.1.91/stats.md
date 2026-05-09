# claude-code 2.1.91 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 18 | 0 | 0 | 6 | 26673 | 2 | 3 | 13 | 1.5s |
| `03-with-mcp` | 1 | 9 | 18 | 0 | 0 | 6 | 26673 | 2 | 3 | 106 | 2.5s |
| `04-with-skill` | 2 | 9 | 18 | 0 | 0 | 6 | 26673 | 2 | 5 | 66 | 7.6s |

## Models seen across scenarios

- `claude-opus-4-6`
