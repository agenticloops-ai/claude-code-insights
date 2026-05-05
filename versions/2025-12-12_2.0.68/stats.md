# claude-code 2.0.68 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 17 | 0 | 0 | 0 | 0 | 12990 | 0 | 738 | 139 | 5.7s |
| `03-with-mcp` | 3 | 17 | 0 | 0 | 0 | 0 | 12990 | 0 | 738 | 172 | 5.1s |
| `04-with-skill` | 5 | 17 | 0 | 0 | 0 | 0 | 12990 | 0 | 1594 | 343 | 11.3s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
