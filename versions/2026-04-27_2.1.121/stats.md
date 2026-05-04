# claude-code 2.1.121 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 10 | 19 | 0 | 89 | 10 | 26719 | 4 | 6 | 16 | 2.7s |
| `03-with-mcp` | 2 | 10 | 19 | 0 | 89 | 10 | 26719 | 4 | 373 | 1970 | 20.0s |
| `04-with-skill` | 3 | 10 | 19 | 0 | 90 | 10 | 26719 | 4 | 364 | 139 | 4.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
