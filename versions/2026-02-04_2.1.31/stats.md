# claude-code 2.1.31 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 17 | 0 | 0 | 0 | 1 | 13970 | 1 | 11 | 13 | 2.3s |
| `03-with-mcp` | 2 | 17 | 0 | 0 | 0 | 1 | 13970 | 1 | 11 | 30 | 5.3s |
| `04-with-skill` | 3 | 17 | 0 | 0 | 0 | 1 | 13970 | 1 | 13 | 65 | 3.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
