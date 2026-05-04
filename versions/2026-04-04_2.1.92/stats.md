# claude-code 2.1.92 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 9 | 0 | 0 | 0 | 6 | 26673 | 3 | 3 | 13 | 5.1s |
| `03-with-mcp` | 1 | 9 | 0 | 0 | 0 | 6 | 26673 | 3 | 3 | 1493 | 14.3s |
| `04-with-skill` | 2 | 9 | 0 | 0 | 0 | 6 | 26673 | 3 | 5 | 66 | 5.2s |

## Models seen across scenarios

- `claude-opus-4-6`
