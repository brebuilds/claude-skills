# Stage — Write Back

## What this stage does
Writes classification record to Stacks Inventory table via Airtable writer tool.

## Inputs
Classification record from classify stage.

## Outputs
Airtable record ID + status (created / updated / skipped-dedup).

## Idempotency
Keyed by content hash. Re-running with same content hash → updates existing row, doesn't create duplicate.

## Failure handling
- Airtable rate limit (429) → back off 1s, retry up to 3×
- Schema mismatch (field renamed, etc.) → log + flag, don't break the batch
- Network error → retry once, then mark as `write-failed` in memory for next-run retry
