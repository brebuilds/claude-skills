# OIB.Guide Listing Drafter — Boundary

## NEVER do

1. **Never publish without `dryRun` preview first.** Even if `/api/publish` is called manually, the request must include `dryRun: true` on the first call. Only on second call (after Bre or the agent has reviewed the preview) is `dryRun: false` allowed. Until the route handler supports `dryRun` (gap #4), this means the agent generates copy + Bre eyeballs + then `/api/publish` runs. No silent-publish path.

2. **Never use banned tourism-board vocabulary.** The list in `voice.md` is final. If the etsy-listing-writer skill output contains any banned term, REGENERATE — do not ship. Banned: tropical paradise, luxury escape, exotic getaway, your slice of heaven, island vibes, aloha, palm trees swaying, endless summer.

3. **Never write SKU strings.** The Printify adapter (`pod-dashboard/src/lib/publish/printify.ts`) owns canonical SKU assembly via the `preflightSkus` + `buildVariantSku` pipeline. This agent only produces listing copy (title/description/tags/attributes). If asked to "generate a SKU for design X" — refuse and route to the publish path.

4. **Never invent location references.** If the design doesn't tie to a real Brunswick County spot, don't add one. Generic beach > fake-specific beach.

5. **Never quote prices in description body.** Prices come from Pricing Rules table at publish time. The agent's description should describe the product, not pricing — pricing tier changes shouldn't break copy.

## Flag to human

- **New product type** the brand voice hasn't been validated for yet — escalate to Bre. The 27 templates cover known territory; anything else needs voice approval first.
- **Design name contains a location that's NOT Brunswick County / NC coast** — flag, because it may be the wrong brand (TFH, FL, DNC, or a sister brand). Voice anchors break if the location is wrong.
- **etsy-listing-writer output flagged as low confidence** — escalate rather than ship.
- **Multiple banned-vocab regenerations in a single design** (>3 attempts and still failing voice check) — stop, flag to Bre, probably means the design's underlying concept doesn't fit OIB voice cleanly.

## Why these are hard

(Fill in after 1-2 real sessions — what almost broke, what surprised you.)
