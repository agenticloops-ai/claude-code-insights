# claude-code 2.1.128 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 11 | 22 | 0 | 0 | 10 | 26719 | 4 | 6 | 15 | 3.7s |
| `03-with-mcp` | 2 | 11 | 22 | 0 | 0 | 10 | 26719 | 4 | 373 | 1970 | 20.4s |
| `04-with-skill` | 3 | 11 | 22 | 0 | 0 | 10 | 26719 | 4 | 364 | 103 | 5.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
