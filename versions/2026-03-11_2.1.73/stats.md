# claude-code 2.1.73 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 27 | 0 | 0 | 4 | 19164 | 2 | 3 | 13 | 5.0s |
| `03-with-mcp` | 1 | 1 | 27 | 0 | 0 | 4 | 19164 | 2 | 3 | 1574 | 14.4s |
| `04-with-skill` | 3 | 1 | 27 | 0 | 0 | 4 | 19164 | 2 | 8 | 142 | 8.0s |

## Models seen across scenarios

- `claude-opus-4-6`
