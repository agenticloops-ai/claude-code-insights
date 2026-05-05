# claude-code 2.1.39 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 2 | 23 | 0 | 0 | 0 | 1 | 18479 | 1 | 11 | 13 | 2.8s |
| `03-with-mcp` | 2 | 23 | 0 | 0 | 0 | 1 | 18479 | 1 | 11 | 1502 | 21.6s |
| `04-with-skill` | 3 | 23 | 0 | 0 | 0 | 1 | 18479 | 1 | 13 | 67 | 5.1s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-6`
