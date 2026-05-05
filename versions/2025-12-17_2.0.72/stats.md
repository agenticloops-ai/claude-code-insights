# claude-code 2.0.72 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 18 | 0 | 0 | 0 | 0 | 13412 | 0 | 779 | 146 | 4.6s |
| `03-with-mcp` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.6s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 13412 | 0 | 1676 | 292 | 11.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
