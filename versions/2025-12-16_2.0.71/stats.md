# claude-code 2.0.71 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 18 | 0 | 0 | 0 | 0 | 13412 | 0 | 779 | 112 | 3.9s |
| `03-with-mcp` | 3 | 18 | 0 | 0 | 0 | 0 | 13412 | 0 | 779 | 170 | 5.1s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 13412 | 0 | 1676 | 273 | 9.2s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
