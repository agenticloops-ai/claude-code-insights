# claude-code 2.1.0 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 17 | 0 | 0 | 0 | 0 | 12699 | 0 | 3766 | 261 | 7.1s |
| `03-with-mcp` | 3 | 17 | 0 | 0 | 0 | 0 | 12699 | 0 | 12 | 181 | 5.5s |
| `04-with-skill` | 6 | 17 | 0 | 0 | 0 | 0 | 12699 | 0 | 3768 | 413 | 11.2s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
