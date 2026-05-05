# claude-code 2.0.74 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 18 | 0 | 0 | 0 | 0 | 13421 | 0 | 771 | 210 | 3.6s |
| `03-with-mcp` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.6s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 13421 | 0 | 1676 | 338 | 12.4s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
