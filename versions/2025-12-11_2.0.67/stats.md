# claude-code 2.0.67 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 17 | 0 | 0 | 0 | 0 | 12773 | 0 | 10 | 13 | 2.5s |
| `03-with-mcp` | 3 | 17 | 0 | 0 | 0 | 0 | 12773 | 0 | 738 | 167 | 4.2s |
| `04-with-skill` | 5 | 17 | 0 | 0 | 0 | 0 | 12773 | 0 | 1594 | 258 | 9.4s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
