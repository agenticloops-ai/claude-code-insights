# claude-code 2.1.92 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 18 | 0 | 0 | 6 | 26673 | 2 | 3 | 13 | 2.6s |
| `03-with-mcp` | 1 | 9 | 18 | 0 | 0 | 6 | 26673 | 2 | 3 | 51 | 8.5s |
| `04-with-skill` | 2 | 9 | 18 | 0 | 0 | 6 | 26673 | 2 | 5 | 65 | 6.9s |

## Models seen across scenarios

- `claude-opus-4-6`
