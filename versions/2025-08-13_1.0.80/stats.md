# claude-code 1.0.80 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 16 | 0 | 0 | 0 | 0 | 12772 | 1 | 2 | 12 | 2.3s |
| `03-with-mcp` | 2 | 16 | 0 | 0 | 0 | 0 | 12772 | 1 | 2 | 29 | 3.4s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-1-20250805`
