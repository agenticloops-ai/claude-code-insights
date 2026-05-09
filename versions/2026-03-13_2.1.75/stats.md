# claude-code 2.1.75 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 1 | 25 | 0 | 0 | 4 | 15786 | 2 | 3 | 13 | 2.1s |
| `03-with-mcp` | 1 | 1 | 25 | 0 | 0 | 4 | 15786 | 2 | 3 | 111 | 3.4s |
| `04-with-skill` | 0 | None | 0 | 0 | 0 | 0 | None | None | None | None | — |

## Models seen across scenarios

- `claude-opus-4-6`
