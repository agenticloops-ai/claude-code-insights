# claude-code 2.1.117 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 19 | 0 | 89 | 10 | 26699 | 4 | 6 | 15 | 1.9s |
| `03-with-mcp` | 2 | 10 | 19 | 0 | 90 | 10 | 26699 | 4 | 373 | 2006 | 22.1s |
| `04-with-skill` | 3 | 10 | 19 | 0 | 89 | 10 | 26699 | 4 | 364 | 142 | 5.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
