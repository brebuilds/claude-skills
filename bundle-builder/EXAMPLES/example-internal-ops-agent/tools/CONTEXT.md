# Stacks Inventory Auditor — Tools

Three load-bearing tools.

## Tools

| Tool | Status | What it does |
|---|---|---|
| `file-walker.md` | needs build (partial — Drive enumeration works, others TBD) | Read-only enumeration of source folders + content hashing |
| `classifier.md` | needs build | Per-file classification (type, brand, readiness) — likely LLM with retrieval over brand context |
| `airtable-writer.md` | exists (uses Airtable MCP) | Write classification back to Stacks Inventory table |

## What we DON'T use here

- File-system mutation tools (mv, rm) — explicitly out of scope per boundary
- Direct Printify / Etsy / Shopify access — that's downstream agents' job
- Brand voice generation — internal-ops doesn't speak to customers

## Tool sequencing

See `pipeline/` for the stage-by-stage flow that uses these three.
