# claude-code 2.1.76 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 0 | 0 | 0 | 4 | 19306 | 2 | 3 | 41 | 3.3s |
| `03-with-mcp` | 1 | 1 | 0 | 0 | 0 | 4 | 19306 | 2 | 3 | 1446 | 13.4s |
| `04-with-skill` | 3 | 1 | 0 | 0 | 0 | 4 | 19306 | 2 | 8 | 142 | 6.9s |

## Models seen across scenarios

- `claude-opus-4-6`
