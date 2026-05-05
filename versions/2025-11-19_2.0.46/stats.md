# claude-code 2.0.46 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 16 | 0 | 0 | 0 | 0 | 11229 | 0 | 600 | 213 | 7.7s |
| `03-with-mcp` | 3 | 16 | 0 | 0 | 0 | 0 | 11229 | 0 | 600 | 190 | 5.4s |
| `04-with-skill` | 5 | 16 | 0 | 0 | 0 | 0 | 11229 | 0 | 1207 | 345 | 15.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
