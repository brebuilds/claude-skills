# OIB.Guide Listing Drafter — Memory

## Per-conversation state
**None.** Each invocation is independent. The agent doesn't carry thread state across calls.

## Per-entity state (per-design × product type × platform)
**Yes — read-only check before drafting.**

Before generating, the agent queries `Listings` table for a row matching:
- `Design` = current design ID
- `Brand` = OIB.Guide
- `Product Type` = current product type
- `Platform` = target platform (Shopify / Etsy / Printify)

If a row already exists with `Sync Status` ∈ {`ready-to-publish`, `published`, `live`}:
- Skip generation
- Return existing row ID
- Log "already drafted, skipping"

This is the de-dup gate. Prevents wasting tokens on designs we've already drafted for that product/platform combo.

## Global learning
**None at this layer.**

Voice corpus + banned vocabulary live in the `brand-oib-guide` skill, not in this agent's memory. The skill IS the global memory. When the skill is refined (via Workstream 5 brand intelligence), this agent inherits the update automatically.

This separation is deliberate:
- Agent memory = ephemeral per-run state (current design, current product type)
- Skill = persistent brand knowledge (voice, banned vocab, examples)

## What lives where (anti-confusion table)

| State | Lives in | Survives between runs? |
|---|---|---|
| Current design ID, product type, target platform | Agent invocation context | No |
| "Already drafted?" check | Airtable Listings table | Yes |
| Brand voice spec | `brand-oib-guide` skill | Yes |
| Banned vocabulary list | `brand-oib-guide` skill | Yes |
| Listing copy structure rules | `etsy-listing-writer` skill | Yes |
| Per-design SKU code | Designs table | Yes |
| Generated draft (before publish) | Airtable Listings row with `Sync Status = ready-to-publish` | Yes |
