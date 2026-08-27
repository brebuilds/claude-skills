# Tool — etsy-listing-writer skill

## Status
Exists at `~/.claude/skills/etsy-listing-writer/SKILL.md`. Brand-agnostic by design.

## What this agent uses it for

Structure the listing copy: title formula, 13 tags strategy (6-tier), 6-section description format, attributes.

## What the skill provides

- 140-character title structure (Title Formula from template + brand voice anchor)
- 13 tags strategy across 6 tiers: brand-specific, product-type, audience, occasion/gift, niche, broad-search
- 6-section description: hook, product details, materials, sizing, care, brand close
- Etsy attribute recommendations (taxonomy ID, who/when made, materials)

## How this agent uses it differently from the default skill use

The skill is brand-agnostic. This agent passes the brand voice (loaded from `brand-vault/voice.md`) as input so the output is OIB-specific.

The skill alone, without `brand-oib-guide` priming, would produce listings that read "Premium quality print-on-demand product" style. Always pair it with the brand skill.

## Output schema

```json
{
  "title": "string, max 140 chars",
  "description": "multi-line string",
  "tags": ["string", "string", ...],  // exactly 13
  "attributes": {
    "taxonomy_id": 0,
    "who_made": "i_did|someone_else|collective",
    "when_made": "made_to_order|...",
    "is_supply": false
  }
}
```

This shape matches `DesignSnapshot.listingCopy` in `pod-dashboard/src/lib/publish/types.ts`.
