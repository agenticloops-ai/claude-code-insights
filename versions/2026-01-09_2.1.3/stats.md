# claude-code 2.1.3 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 17 | 0 | 0 | 0 | 0 | 12699 | 0 | 12 | 206 | 6.1s |
| `03-with-mcp` | 4 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 4053 | 228 | 7.8s |
| `04-with-skill` | 5 | 11 | 0 | 0 | 0 | 0 | 3141 | 0 | 4053 | 248 | 10.1s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
