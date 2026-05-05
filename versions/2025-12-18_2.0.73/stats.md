# claude-code 2.0.73 — capture summary

Baseline scenario: `03-with-mcp` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.8s |
| `03-with-mcp` | 4 | 17 | 0 | 0 | 0 | 0 | 13421 | 0 | 1676 | 353 | 10.7s |
| `04-with-skill` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.6s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
