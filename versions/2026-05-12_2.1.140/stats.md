# claude-code 2.1.140 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 11 | 19 | 0 | 0 | 10 | 26576 | 4 | 6 | 16 | 1.5s |
| `03-with-mcp` | 2 | 11 | 19 | 0 | 0 | 10 | 26576 | 4 | 373 | 55 | 2.7s |
| `04-with-skill` | 3 | 11 | 19 | 0 | 0 | 10 | 26576 | 4 | 364 | 140 | 5.0s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
