# claude-code 2.1.142 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 11 | 22 | 0 | 0 | 10 | 26577 | 4 | 6 | 16 | 2.1s |
| `03-with-mcp` | 2 | 11 | 22 | 0 | 0 | 10 | 26577 | 4 | 471 | 55 | 3.0s |
| `04-with-skill` | 8 | 11 | 22 | 0 | 0 | 10 | 26577 | 4 | 463 | 769 | 18.9s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-7`
