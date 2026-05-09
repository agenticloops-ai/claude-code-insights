# claude-code 2.1.87 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 18 | 0 | 0 | 6 | 26641 | 2 | 3 | 13 | 2.9s |
| `03-with-mcp` | 1 | 9 | 18 | 0 | 0 | 6 | 26641 | 2 | 3 | 51 | 2.4s |
| `04-with-skill` | 2 | 9 | 18 | 0 | 0 | 6 | 26641 | 2 | 5 | 67 | 4.0s |

## Models seen across scenarios

- `claude-opus-4-6`
