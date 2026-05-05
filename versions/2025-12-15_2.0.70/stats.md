# claude-code 2.0.70 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 17 | 0 | 0 | 0 | 0 | 12990 | 0 | 1676 | 256 | 10.2s |
| `03-with-mcp` | 3 | 17 | 0 | 0 | 0 | 0 | 12990 | 0 | 779 | 160 | 4.8s |
| `04-with-skill` | 5 | 17 | 0 | 0 | 0 | 0 | 12990 | 0 | 1676 | 293 | 9.3s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
