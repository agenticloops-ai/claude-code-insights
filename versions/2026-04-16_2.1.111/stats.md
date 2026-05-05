# claude-code 2.1.111 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 22 | 0 | 0 | 10 | 26401 | 4 | 6 | 15 | 2.1s |
| `03-with-mcp` | 2 | 10 | 22 | 0 | 0 | 10 | 26401 | 4 | 373 | 1970 | 20.1s |
| `04-with-skill` | 3 | 10 | 22 | 0 | 0 | 10 | 26401 | 4 | 364 | 141 | 6.3s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
