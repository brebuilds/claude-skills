# Tool — Airtable Writer

## Status
Exists (uses standard Airtable MCP).

## What this agent uses it for
Writes classification back to Stacks Inventory table.

## Schema mapping
(Placeholder — real Stacks Airtable base + table IDs TBD.)

Approximately:
- `File Path` ← file walker output
- `Content Hash` ← for de-dup
- `Type` ← classifier output
- `Brand` ← classifier output
- `Readiness` ← classifier output
- `Confidence` ← classifier output
- `Classified At` ← timestamp
- `Status` ← `auto-tagged` if confidence ≥ threshold, else `needs-review`

## De-dup behavior
Before writing, check if a row with the same Content Hash already exists. If yes, update the existing row's classification (idempotent re-runs don't duplicate rows).
