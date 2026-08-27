# Stage — Classify

## What this stage does
For each file from the walk stage:
1. Check if content hash already has a fresh classification in Inventory table
2. If fresh → skip (de-dup gate)
3. If stale or absent → run classifier
4. Return classification record

## Inputs
- File metadata + preview from walk stage
- Brand context (from `~/claude-memory/4-pod/` and brand skills, loaded once per batch)
- Feedback-loop examples (see `memory/feedback-loop.md`) — verified-correct + verified-incorrect

## Outputs
`{file_metadata + classification}` per classifier output schema.

## Per-file outcome
- `confidence ≥ threshold` → mark `auto-tagged`, write back
- `confidence < threshold` → mark `needs-review`, write back, surface to review queue
- Classifier error → log + flag, skip write-back for this file
