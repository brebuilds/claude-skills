# OIB.Guide Listing Drafter — Triggers

Event-driven. One invocation per (design × product type) pair.

## Invocation patterns

### Manual (today)
Bre or a Claude session calls the agent with:
```
design_id: rec...
product_type_id: rec...
target_platforms: ["shopify", "etsy"]
```
Agent returns the drafted listing copy as JSON or writes it to the Listings table.

### Batch (after Phase 2.4 of AUTONOMY-ROADMAP lands)
A batch-publish runner reads filtered Design rows (e.g., `brand=OIB AND has_source=true AND has_mockup=true`), and for each it calls this agent in parallel (rate-limited — see `queue.md`).

### Recommender-driven (after Project #42 ships)
The POD Recommender Bot picks design × product type pairs based on trend research + performance signals + brand fit, and calls this agent to draft each.

## What this agent does NOT do

- Does not decide which designs to draft for. That's the Recommender's job.
- Does not publish. That's `/api/publish` (and the Printify/Shopify/Etsy adapters underneath).
- Does not handle images. Listing images are a separate agent (mockup pipeline, Workstream 2.5).
- Does not sync orders, monitor sales, or do analytics. Those are Workstream 4.

## See also

- `queue.md` — rate-limit notes for batch invocation (volume scaling axis)
