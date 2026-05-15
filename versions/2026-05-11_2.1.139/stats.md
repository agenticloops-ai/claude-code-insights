# claude-code 2.1.139 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 11 | 19 | 0 | 0 | 10 | 26572 | 4 | 6 | 16 | 1.6s |
| `03-with-mcp` | 2 | 11 | 19 | 0 | 0 | 10 | 26572 | 4 | 373 | 55 | 5.5s |
| `04-with-skill` | 3 | 11 | 19 | 0 | 0 | 10 | 26572 | 4 | 364 | 100 | 7.0s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
