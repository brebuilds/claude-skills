# OIB.Guide Listing Drafter — Routing

## Source of truth

1. **Airtable base** `[production base ID]` (production POD base, single-base architecture per `project_pod_sync_architecture`):
   - `Designs` (`[Designs table ID]`) — design row with brand link, SKU code, category, source files, tags
   - `Listings` (`[Listings table ID]`) — output target; one row per (Design × Brand × Platform) per `oib-shopify-sync/ARCHITECTURE.md`
   - `Listing Templates` (`[Listing Templates table ID]`) — title formulas, base tags, pricing rules, blueprint ID
   - `Brand Info` (`[Brand Info table ID]`, OIB row `[OIB Brand Info record ID]`) — SKU prefix, connections
   - `Product Type` (`[Product Type table ID]`) — codes, blueprints, categories
   - `Categories` (`[Categories table ID]`) — SKU code per category
   - `Pricing Rules` (`[Pricing Rules table ID]`) — markup/min/max per product type
2. **Skills:** `brand-oib-guide`, `etsy-listing-writer`, `pod-listing-pipeline`
3. **Code:** `~/pod-dashboard/src/app/api/publish/route.ts` (the publish entry), `~/pod-dashboard/src/lib/publish/` (orchestrator + adapters)
4. **Memory:** `~/claude-memory/4-pod/oib-guide/` (brand-specific notes), `~/claude-memory/4-pod/SKU-CODES-REVIEW-2026-05-26.md` (canonical SKU baseline)
5. **Gap context:** `~/claude-memory/4-pod/GAP-REPORT-2026-05-26.md` (what's still broken), `~/claude-memory/4-pod/AUTONOMY-ROADMAP.md` (the bigger arc)

## Scattered or duplicated — cleanup flags

- `brand-oib-guide` skill is stale per gap report 4.1 — TODOs for Etsy/Printify/Airtable IDs that are now real. Refresh before relying on it for voice anchoring.
- Two OIB Airtable bases exist: production (`[production base ID]`) and fork (`[fork base ID]`). This agent ONLY reads/writes production. Fork is for separate enrichment work.

## Missing — setup work

- Server-side `listingCopy` generation in `/api/publish` (gap report #5) — currently the route accepts pre-baked copy. This agent's output has to be passed in as `listingCopy: {...}` in the request body until that gap closes.
- `dryRun` mode on `/api/publish` (gap report #4) — without it, this agent can't preview before publishing. Workaround for now: validate output via `/tmp/test-sku-payload.py` style payload inspection.

## Sub-routes

- `brand-vault/` — OIB voice spec + boundary (read-only reference)
- `tools/` — Airtable MCP, brand-oib-guide skill, etsy-listing-writer skill
- `memory/` — what this agent remembers per-design
- `triggers/` — event-driven invocation patterns + queue/rate-limit notes (volume axis)
