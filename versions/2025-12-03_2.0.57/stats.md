# claude-code 2.0.57 — capture summary

Baseline scenario: `03-with-mcp` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 0 | None | 0 | 0 | 0 | 0 | None | None | None | None | — |
| `03-with-mcp` | 3 | 17 | 0 | 0 | 0 | 0 | 12487 | 0 | 740 | 158 | 5.0s |
| `04-with-skill` | 5 | 17 | 0 | 0 | 0 | 0 | 12487 | 0 | 1598 | 333 | 10.4s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
