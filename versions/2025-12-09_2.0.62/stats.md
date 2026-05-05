# claude-code 2.0.62 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 18 | 0 | 0 | 0 | 0 | 12773 | 0 | 738 | 136 | 3.9s |
| `03-with-mcp` | 3 | 18 | 0 | 0 | 0 | 0 | 12773 | 0 | 738 | 238 | 5.1s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 12773 | 0 | 1594 | 358 | 10.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
