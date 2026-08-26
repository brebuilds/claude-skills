# OIB.Guide Listing Drafter

**Built:** 2026-05-26
**Why this exists:** OIB.Guide is the priority brand for summer 2026 tourist revenue. ~712 OIB designs sit in the fork base; production base has 1 design promoted. Mass-publishing requires brand-voiced listing copy at scale. This agent owns that conversion: Design × Product Type → complete Etsy/Shopify listing copy ready for `/api/publish`.
**Scaling axis:** Volume — same job, many more invocations. Build for queues + rate limits.
**Status:** scaffolded — needs 1-2 real session runs to validate

## What this agent does

Drafts a complete, brand-voiced listing for an OIB.Guide design on a specific product type. One agent invocation = one listing row's worth of copy (title, description, 13 tags, attributes).

Single job: draft listing copy.

## Try it

1. Open `CLAUDE.md` in the agent runtime
2. Pick a real Design row from production base (e.g., `[Design record ID]` Ocean Isle Beach, SKU `OCISB`)
3. Pick a real Product Type (e.g., Beach Towel = blueprint 968)
4. Run the agent — it should produce title/description/13 tags/attributes
5. Validate the output via `/tmp/test-sku-payload.py`-style payload inspection (no live publish until `dryRun` mode lands)
6. Note what's missing or wrong
7. Come back to "Builder notes" below

## Builder notes

(Empty — fill in after first 1-2 sessions.)

Likely failure modes to watch:
- Brand voice slip — generic tourism language creeping in despite `brand-oib-guide` anchor
- Tag set leaning generic instead of OIB-hyperlocal
- Pricing pulled from wrong source (template Pricing Rules vs. brand intent)
- Listing copy generated but not written back to Listings table (current gap — see CONTEXT.md "Missing")
