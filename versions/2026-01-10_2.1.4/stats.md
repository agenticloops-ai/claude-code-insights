# claude-code 2.1.4 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 1 | 0 | 0 | 0 | 0 | 1591 | 0 | 4056 | 184 | 6.7s |
| `03-with-mcp` | 3 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 12 | 182 | 5.1s |
| `04-with-skill` | 5 | 1 | 0 | 0 | 0 | 0 | 1591 | 0 | 4056 | 285 | 10.2s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
