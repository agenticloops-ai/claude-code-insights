# claude-code 2.1.75 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 0 | 0 | 0 | 4 | 19306 | 2 | 3 | 41 | 4.8s |
| `03-with-mcp` | 1 | 1 | 0 | 0 | 0 | 4 | 19306 | 2 | 3 | 1482 | 15.9s |
| `04-with-skill` | 3 | 1 | 0 | 0 | 0 | 4 | 19306 | 2 | 8 | 142 | 10.9s |

## Models seen across scenarios

- `claude-opus-4-6`
