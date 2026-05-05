# claude-code 2.0.64 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 18 | 0 | 0 | 0 | 0 | 12773 | 0 | 738 | 127 | 3.9s |
| `03-with-mcp` | 4 | 18 | 0 | 0 | 0 | 0 | 12773 | 0 | 1594 | 312 | 8.6s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 12773 | 0 | 1594 | 323 | 9.3s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
