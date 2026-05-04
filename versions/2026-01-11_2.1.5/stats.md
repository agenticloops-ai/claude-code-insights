# claude-code 2.1.5 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 1 | 0 | 0 | 0 | 0 | 1591 | 0 | 4056 | 226 | 7.9s |
| `03-with-mcp` | 4 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 4056 | 234 | 7.2s |
| `04-with-skill` | 6 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 4058 | 390 | 12.7s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
