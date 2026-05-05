# claude-code 2.0.61 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 3 | 18 | 0 | 0 | 0 | 0 | 12483 | 0 | 738 | 132 | 3.9s |
| `03-with-mcp` | 2 | 18 | 0 | 0 | 0 | 0 | 12483 | 0 | 730 | 235 | 4.9s |
| `04-with-skill` | 4 | 18 | 0 | 0 | 0 | 0 | 12483 | 0 | 1594 | 317 | 9.5s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
