# claude-code 2.1.116 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 20 | 0 | 0 | 10 | 26269 | 3 | 6 | 15 | 2.2s |
| `03-with-mcp` | 2 | 10 | 20 | 0 | 0 | 10 | 26269 | 3 | 373 | 55 | 3.0s |
| `04-with-skill` | 3 | 10 | 20 | 0 | 0 | 10 | 26269 | 3 | 364 | 141 | 4.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
