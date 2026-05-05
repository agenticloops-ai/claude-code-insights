# claude-code 2.1.118 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 22 | 0 | 0 | 10 | 26699 | 4 | 6 | 15 | 2.2s |
| `03-with-mcp` | 2 | 10 | 22 | 0 | 0 | 10 | 26699 | 4 | 373 | 2006 | 20.8s |
| `04-with-skill` | 3 | 10 | 22 | 0 | 0 | 10 | 26699 | 4 | 364 | 141 | 12.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
