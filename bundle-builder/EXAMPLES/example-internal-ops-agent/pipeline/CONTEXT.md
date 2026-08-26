# Stacks Inventory Auditor — Pipeline

Sequenced stages. One invocation runs them in order.

## Stages

1. `walk.md` — enumerate files from configured source folders
2. `classify.md` — for each new/stale file, run the classifier
3. `write-back.md` — write classification back to Stacks Inventory table

## Sequencing rules

- Stages run sequentially per file (not all walk first then all classify)
- Stages are idempotent — re-running on the same file with same content hash → same outcome (no duplicate rows)
- A stage failure → log + flag the file, continue with next file. Whole run shouldn't abort on one file's classify error.

## See also

- `walk.md`, `classify.md`, `write-back.md` for stage details
- `memory/feedback-loop.md` for how classify gets smarter over time
