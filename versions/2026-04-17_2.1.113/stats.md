# claude-code 2.1.113 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 20 | 0 | 0 | 10 | 26401 | 3 | 6 | 13 | 1.9s |
| `03-with-mcp` | 2 | 10 | 20 | 0 | 0 | 10 | 26401 | 3 | 373 | 58 | 3.3s |
| `04-with-skill` | 3 | 10 | 20 | 0 | 0 | 10 | 26401 | 3 | 364 | 101 | 5.5s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
