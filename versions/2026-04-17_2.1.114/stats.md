# claude-code 2.1.114 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 20 | 0 | 0 | 10 | 26401 | 3 | 6 | 15 | 1.5s |
| `03-with-mcp` | 2 | 10 | 20 | 0 | 0 | 10 | 26401 | 3 | 373 | 55 | 7.7s |
| `04-with-skill` | 3 | 10 | 20 | 0 | 0 | 10 | 26401 | 3 | 364 | 102 | 7.1s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
