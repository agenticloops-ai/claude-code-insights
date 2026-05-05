# claude-code 2.0.76 — capture summary

Baseline scenario: `03-with-mcp` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.6s |
| `03-with-mcp` | 3 | 18 | 0 | 0 | 0 | 0 | 13204 | 0 | 738 | 153 | 5.3s |
| `04-with-skill` | 5 | 18 | 0 | 0 | 0 | 0 | 13204 | 0 | 1594 | 284 | 9.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
