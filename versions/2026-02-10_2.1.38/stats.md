# claude-code 2.1.38 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 23 | 0 | 0 | 0 | 1 | 18479 | 1 | 11 | 13 | 2.6s |
| `03-with-mcp` | 2 | 23 | 0 | 0 | 0 | 1 | 18479 | 1 | 11 | 1531 | 22.1s |
| `04-with-skill` | 3 | 23 | 0 | 0 | 0 | 1 | 18479 | 1 | 13 | 67 | 4.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
